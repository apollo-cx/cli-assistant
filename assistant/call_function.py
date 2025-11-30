"""Function call dispatcher for OpenAI tool calls.

This module routes tool calls from the LLM to the appropriate function
implementations, automatically injecting the working directory for security.
"""

import os
import json

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

    if verbose:
        print(f" - Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

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

    return {"result": function_result}
