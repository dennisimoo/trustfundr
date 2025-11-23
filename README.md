# TrustFundr - AI Investment Analyst Agent

An intelligent investment research assistant that combines multiple AI-powered tools to analyze companies and provide investment recommendations. Built with E2B sandboxes, Google ADK, and MCP (Model Context Protocol).

## Features

- 🔍 **Real-time Research** - Uses Perplexity AI to gather current financial data, news, and market information
- 🌐 **Web Scraping** - Leverages Firecrawl to extract detailed company information from websites
- 🤖 **Multi-Tool Orchestration** - Intelligently combines 9 different tools to provide comprehensive analysis
- 🔒 **Secure Execution** - All tool execution happens in isolated E2B sandboxes
- ⚡ **Fast Inference** - Powered by Groq's Llama 3.3 70B for rapid responses
- 📊 **Structured Recommendations** - Clear INVEST/DO NOT INVEST guidance with confidence levels

## Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         v
┌─────────────────────────┐
│   Google ADK Agent      │
│   (Llama 3.3 70B)       │
└────────┬────────────────┘
         │
         v
┌─────────────────────────┐
│   E2B MCP Gateway       │
└────────┬────────────────┘
         │
    ┌────┴────┐
    │         │
    v         v
┌─────────┐ ┌──────────┐
│Perplexity│ │Firecrawl │
│   (3)    │ │   (6)    │
└─────────┘ └──────────┘
```

## Available Tools

### Perplexity Tools (3)
- `perplexity_ask` - AI-powered search and Q&A
- `perplexity_reason` - Deep reasoning capabilities
- `perplexity_research` - Comprehensive research queries

### Firecrawl Tools (6)
- `firecrawl_scrape` - Scrape individual web pages
- `firecrawl_crawl` - Crawl entire websites
- `firecrawl_search` - Search and scrape results
- `firecrawl_map` - Map website structure
- `firecrawl_extract` - Extract structured data
- `firecrawl_check_crawl_status` - Monitor crawl progress

## Prerequisites

- Python 3.10+
- API Keys:
  - [E2B API Key](https://e2b.dev)
  - [Groq API Key](https://console.groq.com)
  - [Perplexity API Key](https://www.perplexity.ai/settings/api)
  - [Firecrawl API Key](https://firecrawl.dev)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dennisimoo/trustfundr.git
cd trustfundr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` files:

**Root `.env`:**
```bash
E2B_API_KEY=your_e2b_key
GROQ_API_KEY=your_groq_key
PERPLEXITY_API_KEY=your_perplexity_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

**`my_agent/.env`:**
```bash
E2B_API_KEY=your_e2b_key
GROQ_API_KEY=your_groq_key
PERPLEXITY_API_KEY=your_perplexity_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

## Usage

### Start the Agent

Run the startup script:
```bash
./run.sh
```

This will:
1. Start the E2B sandbox with MCP servers
2. Launch the Google ADK web interface at `http://127.0.0.1:8000`
3. Display available tools in the terminal

### Example Queries

**Simple Greeting:**
```
User: Hi!
Agent: Hello! I'm your investment analyst assistant...
```

**Company Analysis:**
```
User: Should I invest in Tesla?
Agent: [Researches using Perplexity and Firecrawl]

INVEST - Medium Confidence

Key Strengths:
- Strong revenue growth (45% YoY)
- Market leader in EV sector
- Innovative leadership team

Key Risks:
- High valuation metrics
- Competition intensifying
- Regulatory challenges

[Full analysis with sources...]
```

**Private Company:**
```
User: What do you think about investing in Anthropic?
Agent: [Adapts to limited public data for private companies]
```

## Project Structure

```
trustfundr/
├── main.py                 # E2B sandbox setup with MCP servers
├── run.sh                  # Startup script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── my_agent/
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # ADK agent definition
│   ├── mcp_config.json    # MCP gateway config (auto-generated)
│   └── .env               # Agent environment variables
├── .env                   # Root environment variables
└── README.md              # This file
```

## How It Works

1. **E2B Sandbox Creation** - `main.py` creates an isolated sandbox with Perplexity and Firecrawl MCP servers
2. **MCP Gateway Export** - The sandbox exports an HTTP gateway URL and authentication token
3. **ADK Agent Connection** - The Google ADK agent connects to the MCP gateway via StreamableHTTP
4. **Tool Discovery** - The agent automatically discovers all 9 available tools
5. **LLM Orchestration** - Llama 3.3 70B decides which tools to call based on user queries
6. **Secure Execution** - All tool calls execute in the E2B sandbox
7. **Response Generation** - Results are synthesized into actionable investment insights

## Technical Stack

- **[E2B](https://e2b.dev)** - Secure cloud sandboxes for AI agents
- **[MCP](https://modelcontextprotocol.io)** - Model Context Protocol for tool integration
- **[Google ADK](https://github.com/google/adk)** - Agent Development Kit framework
- **[Groq](https://groq.com)** - Ultra-fast LLM inference (Llama 3.3 70B)
- **[Perplexity](https://www.perplexity.ai)** - AI-powered research and search
- **[Firecrawl](https://firecrawl.dev)** - Web scraping and crawling service
- **[LiteLLM](https://litellm.ai)** - Unified LLM API interface

## Configuration

### Model Selection

Edit `my_agent/agent.py` to change the LLM:
```python
root_agent = Agent(
    model=LiteLlm(
        model="groq/llama-3.3-70b-versatile",  # Change model here
        api_key=os.getenv("GROQ_API_KEY"),
    ),
    # ...
)
```

Available Groq models:
- `groq/llama-3.3-70b-versatile` (best for tool calling)
- `groq/llama-3.1-70b-versatile`
- `groq/llama-3.1-8b-instant` (faster, lower cost)

### System Prompt

Customize the investment analyst behavior in `my_agent/agent.py`:
```python
SYSTEM_PROMPT = """You are an investment analyst AI..."""
```

### MCP Servers

Add or remove MCP servers in `main.py`:
```python
sbx = await AsyncSandbox.create(mcp={
    "perplexityAsk": {
        "perplexityApiKey": os.getenv("PERPLEXITY_API_KEY"),
    },
    "firecrawl": {
        "apiKey": os.getenv("FIRECRAWL_API_KEY"),
        "url": "https://api.firecrawl.dev",
        # ... additional config
    },
    # Add more MCP servers here
})
```

## Troubleshooting

### Rate Limits
If you hit Groq rate limits:
- Wait the specified time (usually 30-60 seconds)
- Upgrade to Groq's dev tier for higher limits
- Switch to a smaller/faster model like `llama-3.1-8b-instant`

### Tool Validation Errors
If you see "tool calling not supported" or validation errors:
- Ensure you're using a model that supports function calling
- Check that tool names don't have unsupported characters
- Verify all API keys are correct

### Firecrawl "Unauthorized" Errors
- Verify your Firecrawl API key is correct (starts with `fc-`, not `gsk_`)
- Check your Firecrawl account has available credits
- Ensure the API key is set in both `.env` files

### Connection Issues
- Confirm E2B sandbox is running (check terminal output)
- Verify `mcp_config.json` was created in `my_agent/`
- Check that port 8000 is not already in use

## Development

### Running in Development Mode

```bash
# Run main.py separately
python3 main.py

# In another terminal, run ADK web
cd my_agent
adk web
```

### Adding New Tools

1. Add MCP server configuration to `main.py`
2. Restart the sandbox
3. Tools are automatically discovered by the agent

### Modifying the Agent

Edit `my_agent/agent.py` to:
- Change the system prompt
- Adjust model parameters
- Add custom tool filters
- Modify timeout settings

## Video Demo

See `VIDEO_SCRIPT.md` for a complete demo script showing:
- Simple greeting (no tool calls)
- Tesla investment analysis
- Palantir deep dive
- Anthropic (private company) analysis
- Architecture walkthrough

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

Built by [Dennis](https://github.com/dennisimoo) with assistance from Claude Code.

**Disclaimer:** This tool provides analysis for educational purposes only. Not financial advice. Always do your own research and consult with qualified financial advisors before making investment decisions.

## Resources

- [E2B Documentation](https://e2b.dev/docs)
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Groq Documentation](https://console.groq.com/docs)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

---

**Star ⭐ this repo if you find it useful!**
