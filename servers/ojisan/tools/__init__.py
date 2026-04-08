from fastmcp import FastMCP
from .date_convertor_by_unix import register_date_convertor_by_unix_tool
from .document_translator import register_document_translator_tool
from .file_save import register_file_save
from .file_inspector import register_file_inspector_tool
from .update_local_repository import register_update_local_repository

def register_tools(mcp: FastMCP):
    """
    ツールの一括登録を実行します。
    """
    register_date_convertor_by_unix_tool(mcp)
    register_document_translator_tool(mcp)
    register_file_save(mcp)
    register_file_inspector_tool(mcp)
    register_update_local_repository(mcp)