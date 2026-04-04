import os
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.types import ChatMessage

_client = None

def get_client() -> BasicMCPClient:
    """
    FastMCP Client
    """
    global _client
    if isinstance(_client, BasicMCPClient):
        return _client

    # new Client
    _client = BasicMCPClient(command_or_url=os.getenv("MCP_SERVER_TRANSPORT", "http://localhost:8000/mcp"))

    return _client

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

async def get_tools() -> list[FunctionTool]:
    """
    MCP から Tool リストを取得する。
    """
    client = get_client()
    mcp_tool_spec = McpToolSpec(client=client)
    return await mcp_tool_spec.to_tool_list_async()