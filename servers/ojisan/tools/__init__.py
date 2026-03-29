from fastmcp import FastMCP
from .fileinfo import register_fileinfo_tool

def register_tools(mcp: FastMCP):
    """
    ツールの一括登録を実行します。
    """
    register_fileinfo_tool(mcp)