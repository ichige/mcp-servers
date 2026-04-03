from fastmcp import FastMCP
from .url_validator import register_url_validator

def register_prompts(mcp: FastMCP):
    """
    各 prompts を登録します。
    """
    register_url_validator(mcp)