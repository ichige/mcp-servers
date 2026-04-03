import os
from fastmcp import Client
from mcp.types import GetPromptResult

_client = None

def get_client() -> Client:
    """
    FastMCP Client
    """
    global _client
    if isinstance(_client, Client):
        return _client

    # new Client
    _client = Client(transport=os.getenv("MCP_SERVER_TRANSPORT", "http://localhost:8000/mcp"))

    return _client

