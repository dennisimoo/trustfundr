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
        headers={"Authorization": f"Bearer {mcp_config['token']}"}
    )

    mcp_toolset = McpToolset(
        connection_params=connection_params,
        tool_name_prefix="perplexity_"
    )
    tools.append(mcp_toolset)

root_agent = Agent(
    model=LiteLlm(model="groq/llama-3.3-70b-versatile"),
    name='root_agent',
    description='A helpful assistant with access to Perplexity search tools.',
    instruction='Answer user questions to the best of your knowledge. Use the Perplexity tools for web search and research when needed.',
    tools=tools,
)
