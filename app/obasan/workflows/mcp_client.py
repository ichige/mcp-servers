import os
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.types import ChatMessage
from fastmcp import Client
from fastmcp.client.sampling.handlers.google_genai import GoogleGenaiSamplingHandler
from fastmcp.client.elicitation import ElicitResult, ElicitRequestParams, RequestContext
from typing import Callable, TypeVar, ParamSpec, Awaitable, Any, Optional
from functools import wraps
from obasan.components import show_dialog

_client = None
_mcp_client = None

def get_client() -> BasicMCPClient:
    """
    Basic MCP Client
    """
    global _client
    if isinstance(_client, BasicMCPClient):
        return _client

    # new Client
    _client = BasicMCPClient(command_or_url=os.getenv("MCP_SERVER_TRANSPORT", "http://localhost:8000/mcp"))

    return _client

async def elicitation_handler(
    message: str,
    response_type: type | None,
    params: ElicitRequestParams,
    context: RequestContext
) -> ElicitResult | object:
    """
    User Elicitation のハンドラ
    いわゆる Human-in-the-loop
    本来であれば、response_type や params を見ながら、UIを構成するべきである。
    """

    # 今回は簡易的なダイアログで対応する
    user_input = await show_dialog(message)
    # 承諾
    if user_input == "Yes":
        return ElicitResult(action="accept")
    # 拒否
    if user_input == "No":
        return ElicitResult(action="decline")
    # キャンセル
    return ElicitResult(action="cancel")

def get_mcp_client() -> Client:
    """
    FastMCP Client
    """
    global _mcp_client
    if isinstance(_mcp_client, Client):
        return _mcp_client

    _mcp_client = Client(
        transport=os.getenv("MCP_SERVER_TRANSPORT", "http://localhost:8000/mcp"),
        sampling_handler=GoogleGenaiSamplingHandler(
            default_model=os.getenv("GEMINI_FLASH_LITE_MODEL", "gemini-3.1-flash-lite-preview")
        ),
        elicitation_handler=elicitation_handler,
    )

    return _mcp_client

async def get_prompt(name: str, arguments: Optional[dict] = None) -> str:
    """
    MCP から prompt を取得する
    prompt が1つの場合のみ対応。
    """
    prompt = ""
    client = get_client()
    prompts: list[ChatMessage] = await client.get_prompt(prompt_name=name, arguments=arguments)
    for message in prompts:
        prompt += str(message.content) + "\n"

    return prompt

P = ParamSpec("P")
R = TypeVar("R")

def mcp_sampling_bridge(tool_names: set[str]):
    """
    MCP の特定の Tool 呼び出しで Sampling 対応の FastMCP Client へ差し替えます
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """
        Decorator
        """
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            tools = await func(*args, **kwargs)
            for i, tool in enumerate(tools):
                if isinstance(tool, FunctionTool):
                    if tool.metadata.name in tool_names:
                        # async_fn を差し替えることで、client を sampling 対応に変更できる。
                        async def wrapper_fn(*args: Any,  _name = tool.metadata.name, **kwargs: Any):
                            async with get_mcp_client() as client:
                                return await  client.call_tool(_name, kwargs)

                        # FunctionTool を再生成させる。
                        tools[i] = FunctionTool.from_defaults(
                            tool_metadata=tool.metadata,
                            async_fn=wrapper_fn,
                            fn=tool.fn,
                            partial_params=tool.partial_params,
                            callback=tool._callback,
                            async_callback=tool._async_callback,
                        )

            return tools
        return wrapper
    return decorator

@mcp_sampling_bridge(tool_names={"DocumentTranslator", "UpdateLocalRepository"})
async def get_tools() -> list[FunctionTool]:
    """
    MCP から Tool リストを取得する。
    """
    client = get_client()
    mcp_tool_spec = McpToolSpec(client=client)
    return await mcp_tool_spec.to_tool_list_async()

async def direct_call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """
    FastMCP Clientを利用した直接ツール実行
    """
    async with get_mcp_client() as client:
        result = await client.call_tool(
            name=name,
            arguments=arguments
        )

        if result.is_error:
            raise Exception(f"tool calling {name} failed")

        return result.structured_content