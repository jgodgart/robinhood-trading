import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("https://agent.robinhood.com/mcp/trading") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"Tool: {tool.name}, desc: {tool.description}")

asyncio.run(main())
