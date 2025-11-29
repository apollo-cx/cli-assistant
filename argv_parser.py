import argparse

parser = argparse.ArgumentParser(description="AI Coding Agent")

parser.add_argument("prompt", nargs="*", help="User prompt for the AI agent")

parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output"
)

parser.add_argument("-s", "--silent", action="store_true", help="Enable silent mode")
