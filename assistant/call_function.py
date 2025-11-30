"""Function call dispatcher for OpenAI tool calls.

This module routes tool calls from the LLM to the appropriate function
implementations, automatically injecting the working directory for security.
"""

import os
import json
import time

from assistant.ui import (
    console,
    print_function_call,
    print_function_complete,
    function_calls_panel,
)

from assistant.functions.get_file_content import get_file_content
from assistant.functions.get_files_info import get_files_info
from assistant.functions.run_python import run_python
from assistant.functions.write_file_content import write_file

from assistant.config import WORKING_DIR


def call_function(tool_call, verbose=False):
    """Execute a function based on an OpenAI tool call.

    Args:
        tool_call: OpenAI tool call object containing function name and arguments.
        verbose: If True, print detailed information about the function call.

    Returns:
        Dictionary with either:
        - {"result": <function_output>} on success
        - {"error": <error_message>} if function is unknown

    The working directory is automatically injected into the function arguments
    to enforce sandboxing and prevent access outside the permitted directory.
    """
    function_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    with function_calls_panel() as renderables:
        from rich.text import Text as RichText

        # Add function call info
        call_text = RichText()
        call_text.append("▸ ", style="bold magenta")
        call_text.append(function_name, style="cyan")
        call_text.append(" ", style="")
        call_text.append(str(args), style="dim cyan")
        renderables.append(call_text)

        # Start timing
        start_time = time.time()

        # Execute function
        args["working_directory"] = WORKING_DIR

        function_map = {
            "get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "write_file": write_file,
            "run_python": run_python,
        }

        if function_name not in function_map:
            return {"error": f"Unknown function: {function_name}"}

        function_result = function_map[function_name](**args)

        # Ensure minimum execution time for visibility
        elapsed = time.time() - start_time
        if elapsed < 0.2:
            time.sleep(0.2 - elapsed)

        # Add completion message
        complete_text = RichText()
        complete_text.append("✓ ", style="bold green")
        complete_text.append(function_name, style="cyan")
        complete_text.append(" completed", style="green")
        renderables.append(complete_text)

    return {"result": function_result}
