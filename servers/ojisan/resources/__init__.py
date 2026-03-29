from fastmcp import FastMCP
from .original import register_original_resource

def register_resources(mcp: FastMCP):
    """
    リソースの一括登録を実行します。
    """
    register_original_resource(mcp)