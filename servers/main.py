from fastmcp import FastMCP

mcp = FastMCP("FastMCP Server")

@mcp.tool
def great(name: str) -> str:
    """
    Greets the user
    """
    return f"Hello {name}!"

# Run the server
if __name__ == "__main__":
    mcp.run()