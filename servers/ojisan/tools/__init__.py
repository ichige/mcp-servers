from fastmcp import FastMCP
from .file_save import register_file_save
from .fileinfo import register_fileinfo_tool
from .update_docs import register_update_docs

def register_tools(mcp: FastMCP):
    """
    ツールの一括登録を実行します。
    """
    register_file_save(mcp)
    register_fileinfo_tool(mcp)
    register_update_docs(mcp)