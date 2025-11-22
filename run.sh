#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting E2B MCP Gateway...${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start main.py in the background
cd "$SCRIPT_DIR"
python3 main.py &
MAIN_PID=$!

# Wait a bit for the sandbox to initialize
sleep 5

# Get the MCP URL from the output
echo -e "${BLUE}E2B MCP Gateway started (PID: $MAIN_PID)${NC}"
echo -e "${GREEN}Starting Google ADK Web Interface...${NC}"

# Cleanup function
cleanup() {
    echo -e "\n${BLUE}Shutting down...${NC}"
    kill $MAIN_PID 2>/dev/null
    exit 0
}

# Set up trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start Google ADK web interface from the parent directory
cd "$SCRIPT_DIR"
adk web

# Cleanup when ADK exits
cleanup
