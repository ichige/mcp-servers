from fastmcp import FastMCP
from .file_inspect import register_file_inspect
from .tool_agent import register_tool_agent
from .url_validator import register_url_validator

def register_prompts(mcp: FastMCP):
    """
    各 prompts を登録します。
    """
    register_file_inspect(mcp)
    register_tool_agent(mcp)
    register_url_validator(mcp)