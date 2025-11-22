import asyncio
import os
import logging
from datetime import timedelta
from dotenv import load_dotenv
from e2b import AsyncSandbox
from google.adk.mcp.client import MCPClient
from my_agent.agent import root_agent

# Suppress SSE error logging
logging.getLogger("mcp.client.streamable_http").setLevel(logging.CRITICAL)

load_dotenv()

async def main():
    # Create sandbox with Perplexity MCP
    print("Creating E2B sandbox with Perplexity MCP...")
    sbx = await AsyncSandbox.create(mcp={
        "perplexityAsk": {
            "perplexityApiKey": os.getenv("PERPLEXITY_API_KEY"),
        },
    })

    try:
        # Get MCP gateway details
        mcp_url = sbx.get_mcp_url()
        mcp_token = await sbx.get_mcp_token()

        print(f"MCP Gateway URL: {mcp_url}")

        # Connect ADK agent to the MCP gateway
        print("Connecting agent to MCP gateway...")
        async with MCPClient(
            url=mcp_url,
            headers={"Authorization": f"Bearer {mcp_token}"}
        ) as mcp_client:
            # List available tools
            tools = await mcp_client.list_tools()
            print(f"\nAvailable MCP tools ({len(tools)} total):")
            for tool in tools:
                print(f"  - {tool['name']}")

            # Connect tools to the agent
            root_agent.connect_mcp(mcp_client)

            print("\n" + "="*60)
            print("Agent is ready! Type your questions (or 'quit' to exit)")
            print("="*60 + "\n")

            # Interactive chat loop
            while True:
                try:
                    user_input = input("You: ").strip()
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break

                    if not user_input:
                        continue

                    print("Agent: ", end="", flush=True)

                    # Run the agent
                    response = await root_agent.run(user_input)
                    print(response)
                    print()

                except KeyboardInterrupt:
                    print("\n\nExiting...")
                    break

    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        # Properly kill the sandbox
        print("Killing sandbox...")
        await sbx.kill()
        print("Sandbox killed.")

if __name__ == "__main__":
    asyncio.run(main())
