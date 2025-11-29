import os

from google import genai
from google.genai import types  # type: ignore

from assistant.ui import console, print_function_call, print_function_complete

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


def call_function(function_call_part, verbose=False, plain=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)

    if plain:
        # Plain text output without spinner
        print_function_call(function_name, args, plain=True)
    else:
        # Rich formatted with spinner
        spinner_text = print_function_call(function_name, args, plain=False)
        with console.status(spinner_text, spinner="dots"):
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

        # Show completion
        print_function_complete(function_name, plain=False)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

    # Plain mode execution
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
    print_function_complete(function_name, plain=True)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
