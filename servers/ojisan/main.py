from fastmcp import FastMCP
from ojisan.resources import register_resources
from ojisan.tools import register_tools
from ojisan.prompts import register_prompts

mcp = FastMCP("FastMCP Server")

# Resources
register_resources(mcp)
# Tools
register_tools(mcp)
# Prompts
register_prompts(mcp)

@mcp.tool
def great(name: str) -> str:
    """
    Greets the user
    """
    return f"Hello {name}!"
