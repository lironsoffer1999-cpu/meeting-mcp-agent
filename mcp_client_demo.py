import asyncio

from fastmcp import Client
from mcp_server import mcp


async def main() -> None:
    """
    Demonstrates that the client can connect to the Meeting MCP server
    and discover the available MCP tools.
    This import-based demo is stable on Windows.
    """
    async with Client(mcp) as client:
        tools = await client.list_tools()

        print("Meeting MCP Agent - Available MCP Tools:")
        for tool in tools:
            print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())

# formatting verification
