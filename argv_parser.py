import argparse

parser = argparse.ArgumentParser(description="AI Coding Agent")

parser.add_argument("prompt", nargs="*", help="User prompt for the AI agent")

parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose output"
)

parser.add_argument("-s", "--silent", action="store_true", help="Enable silent mode")

parser.add_argument(
    "--max-chars",
    type=int,
    help="Maximum characters to read from files (overrides config)",
)

parser.add_argument(
    "--working-dir",
    type=str,
    help="Working directory for file operations (overrides config)",
)

parser.add_argument(
    "--iteration-limit",
    type=int,
    help="Maximum number of iterations (overrides config)",
)

parser.add_argument(
    "--min-iterations",
    type=int,
    help="Minimum number of iterations before allowing early exit",
)

parser.add_argument(
    "--model",
    type=str,
    default="gemini-2.0-flash-001",
    help="Model to use for generation",
)
