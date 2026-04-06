import os
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.types import ChatMessage
from fastmcp import Client
from fastmcp.client.sampling.handlers.google_genai import GoogleGenaiSamplingHandler
from typing import Callable, TypeVar, ParamSpec, Awaitable, Any
from functools import wraps

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
    )

    return _mcp_client

async def get_prompt(name: str, arguments: dict) -> str:
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

@mcp_sampling_bridge(tool_names={"DocumentTranslator"})
async def get_tools() -> list[FunctionTool]:
    """
    MCP から Tool リストを取得する。
    """
    client = get_client()
    mcp_tool_spec = McpToolSpec(client=client)
    return await mcp_tool_spec.to_tool_list_async()
