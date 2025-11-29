import os

from google import genai
from google.genai import types  # type: ignore

from assistant.functions.get_file_content import (
    get_file_content,
    schema_get_file_content,
)
from assistant.functions.get_files_info import get_files_info, schema_get_files_info
from assistant.functions.run_python import run_python, schema_run_python
from assistant.functions.write_file_content import write_file, schema_write_file

from assistant.config import WORKING_DIR


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )

    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    args = dict(function_call_part.args)

    args["working_directory"] = WORKING_DIR

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python": run_python,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
