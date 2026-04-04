from fastmcp import FastMCP
from .file_save import register_file_save
from .file_inspector import register_file_inspector_tool
from .update_docs import register_update_docs

def register_tools(mcp: FastMCP):
    """
    ツールの一括登録を実行します。
    """
    register_file_save(mcp)
    register_file_inspector_tool(mcp)
    register_update_docs(mcp)