import json
import os
from pathlib import Path
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

# Read MCP config if it exists
mcp_config_path = Path(__file__).parent / "mcp_config.json"
tools = []

if mcp_config_path.exists():
    with open(mcp_config_path, "r") as f:
        mcp_config = json.load(f)

    # Create MCP toolset with StreamableHTTP connection
    connection_params = StreamableHTTPConnectionParams(
        url=mcp_config["url"],
        headers={"Authorization": f"Bearer {mcp_config['token']}"},
        timeout=60  # Increase timeout to 60 seconds
    )

    mcp_toolset = McpToolset(
        connection_params=connection_params,
    )
    tools.append(mcp_toolset)

SYSTEM_PROMPT = """You are an investment analyst AI. For greetings, respond directly. For investment questions:

1. Use Perplexity tools to research financials, news, and market data
2. Use Firecrawl to scrape company websites for leadership info
3. Provide clear recommendation: INVEST or DO NOT INVEST with confidence level, key strengths/risks, leadership assessment, and sources

Be thorough but concise. This is analysis, not financial advice."""

root_agent = Agent(
    model=LiteLlm(
        model="groq/llama-3.3-70b-versatile",  # Llama 3.3 70B - best tool calling on Groq
        api_key=os.getenv("GROQ_API_KEY"),  # Explicitly pass API key
    ),
    name='root_agent',
    description='A helpful assistant with access to Perplexity search and Firecrawl tools.',
    instruction=SYSTEM_PROMPT,
    tools=tools,
)
