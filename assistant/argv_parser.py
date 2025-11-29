import argparse

parser = argparse.ArgumentParser(description="AI Coding Agent")

parser.add_argument("prompt", nargs="*", help="User prompt for the AI agent")

parser.add_argument(
    "-c", "--clear", action="store_true", help="Clear conversation history"
)


parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output"
)

parser.add_argument("-s", "--silent", action="store_true", help="Enable silent mode")

parser.add_argument(
    "--plain", action="store_true", help="Disable rich formatting (plain text output)"
)
