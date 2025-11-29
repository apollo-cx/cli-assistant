import os
import sys
from dotenv import load_dotenv  # type: ignore
from google import genai
from google.genai import types  # type: ignore

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file_content import schema_write_file
from functions.run_python import schema_run_python

from call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

IMPORTANT: Whenever you produce a function call plan, also include a single short text summary (1-2 sentences) describing the chosen action/intent. The client will use the function_calls to decide what to run, but always return a short text explanation as well.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)


def _parse_args(argv):
    user_prompt = ""
    flags = []

    for arg in argv:
        if arg.startswith("-") or arg.startswith("--"):
            flags.append(arg)
        else:
            user_prompt += arg + " "
    return user_prompt, flags


def generate_response(client, messages, is_verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    tool_responses = []

    if not response.function_calls and response.text:
        return response.text
    else:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=is_verbose)

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

    user_prompt, flags = _parse_args(sys.argv[1:])

    if not user_prompt:
        print("Please provide input text as a command-line argument.")
        sys.exit(1)

    is_verbose = "--verbose" in flags or "-v" in flags

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        final_text = generate_response(client, messages, is_verbose)
        if final_text:
            print("Final response:")
            print(final_text)
            break


if __name__ == "__main__":
    main()
