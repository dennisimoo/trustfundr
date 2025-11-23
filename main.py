import asyncio
import os
import logging
from datetime import timedelta
from dotenv import load_dotenv
from e2b import AsyncSandbox
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

# Suppress SSE error logging
logging.getLogger("mcp.client.streamable_http").setLevel(logging.CRITICAL)

load_dotenv()

async def main():
    # Create sandbox with Perplexity and Firecrawl MCP servers
    sbx = await AsyncSandbox.create(mcp={
        "perplexityAsk": {
            "perplexityApiKey": os.getenv("PERPLEXITY_API_KEY"),
        },
        "firecrawl": {
            "apiKey": os.getenv("FIRECRAWL_API_KEY"),
            "url": "https://api.firecrawl.dev",
            "creditCriticalThreshold": 100,
            "creditWarningThreshold": 500,
            "retryBackoffFactor": 2,
            "retryDelay": 1000,
            "retryMax": 3,
            "retryMaxDelay": 10000,
        },
    })

    try:
        # Get MCP gateway details
        mcp_url = sbx.get_mcp_url()
        mcp_token = await sbx.get_mcp_token()

        print(f"MCP Gateway URL: {mcp_url}")

        # Write MCP connection details to a file for the agent to use
        with open("my_agent/mcp_config.json", "w") as f:
            import json
            json.dump({
                "url": mcp_url,
                "token": mcp_token
            }, f)
        print("MCP config written to my_agent/mcp_config.json")

        # Connect to MCP gateway and list tools
        async with streamablehttp_client(
            url=mcp_url,
            headers={"Authorization": f"Bearer {mcp_token}"},
            timeout=timedelta(seconds=600)
        ) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Small delay to ensure MCP servers are ready
                await asyncio.sleep(1)
                tools = await session.list_tools()
                if tools.tools:
                    print(f"Available tools ({len(tools.tools)} total):")
                    for tool in tools.tools:
                        print(f"  - {tool.name}")
                else:
                    print("Available tools: []")

                print("\nSandbox is running. Press Ctrl+C to stop...")

                # Keep the sandbox running until Ctrl+C
                try:
                    while True:
                        await asyncio.sleep(1)
                except asyncio.CancelledError:
                    print("\nShutting down...")
                    raise
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Properly kill the sandbox
        print("Killing sandbox...")
        await sbx.kill()
        print("Sandbox killed.")

if __name__ == "__main__":
    asyncio.run(main())