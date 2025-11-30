"""Configuration settings for the AI assistant.

Defines:
- File reading limits
- Working directory sandboxing
- Iteration limits for the conversation loop
- System prompt that defines the AI's behavior and capabilities
"""

# Maximum number of characters to read from a file before truncating
MAX_CHARS = 1000000

# Working directory - all file operations are restricted to this path
WORKING_DIR = "./calculator"

# Maximum number of LLM response iterations per user query
ITERATION_LIMIT = 100

# System prompt that defines the AI assistant's role and capabilities
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

IMPORTANT: Whenever you produce a function call plan, also include a single short text summary (1-2 sentences) describing the chosen action/intent. The client will use the function_calls to decide what to run, but always return a short text explanation as well.
"""
