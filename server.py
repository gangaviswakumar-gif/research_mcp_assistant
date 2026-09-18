from mcp.server import MCPServer

# Create the MCP server
mcp = MCPServer("Research Assistant")


@mcp.tool()
def hello_research() -> str:
    """Check whether the Research Assistant MCP server is running."""
    return "Research Assistant MCP Server is running successfully!"


if __name__ == "__main__":
    mcp.run()