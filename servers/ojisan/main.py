from fastmcp import FastMCP
from ojisan.resources import register_resources

mcp = FastMCP("FastMCP Server")

register_resources(mcp)

@mcp.tool
def great(name: str) -> str:
    """
    Greets the user
    """
    return f"Hello {name}!"
