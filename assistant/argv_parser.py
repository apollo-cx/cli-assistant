"""Command-line argument parser for the AI assistant.

Defines the CLI interface for the assistant, supporting:
- User prompts (positional arguments)
- Conversation history clearing
- Verbose output mode
- Silent mode (reserved for future use)
"""

import argparse

parser = argparse.ArgumentParser(
    description="AI Coding Agent - Local LLM-powered coding assistant",
    epilog="Example: ai 'list all Python files'",
)

parser.add_argument("prompt", nargs="*", help="User prompt for the AI agent")

parser.add_argument(
    "-c", "--clear", action="store_true", help="Clear conversation history"
)


parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output"
)

parser.add_argument("-s", "--silent", action="store_true", help="Enable silent mode")
