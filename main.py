import os
import sys

from dotenv import load_dotenv  # type: ignore
from google import genai
from google.genai import types  # type: ignore

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file_content import schema_write_file
from functions.run_python import schema_run_python

from argv_parser import parser
from call_function import call_function
from config import (
    SYSTEM_PRPOMPT as system_prompt,
    MAX_CHARS,
    WORKING_DIR,
    ITERATON_LIMIT,
)

load_dotenv()

_api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=_api_key)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)


def generate_response(client, messages, config_overrides, is_verbose=False):
    response = client.models.generate_content(
        model=config_overrides["model"],
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if not response or not response.candidates:
        print("Warning: Received empty response from API")
        return None

    for candidate in response.candidates:
        messages.append(candidate.content)

    tool_responses = []

    if not response.function_calls and response.text:
        return response.text
    else:
        for function_call in response.function_calls:
            function_call_result = call_function(
                function_call, config_overrides, verbose=is_verbose
            )

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise RuntimeError("Function call did not return a function_response")

            tool_responses.append(function_call_result.parts[0])
            if is_verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(
            types.Content(
                role="user",
                parts=tool_responses,
            )
        )

    return None


def main():

    args = parser.parse_args()
    user_prompt = " ".join(args.prompt) if args.prompt else ""
    is_verbose = args.verbose
    is_silent = args.silent

    # Build config overrides dict with defaults from config.py
    config_overrides = {
        "max_chars": args.max_chars if args.max_chars else MAX_CHARS,
        "working_dir": args.working_dir if args.working_dir else WORKING_DIR,
        "iteration_limit": (
            args.iteration_limit if args.iteration_limit else ITERATON_LIMIT
        ),
        "min_iterations": args.min_iterations if args.min_iterations else 0,
        "model": args.model,
    }

    if not user_prompt:
        print("Please provide input text as a command-line argument.")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for iteration in range(config_overrides["iteration_limit"]):
        final_text = generate_response(client, messages, config_overrides, is_verbose)
        if final_text and iteration >= config_overrides["min_iterations"]:
            print("Final response:")
            print(final_text)
            break


if __name__ == "__main__":
    main()
