import os
import sys
from dotenv import load_dotenv  # type: ignore
from google import genai
from google.genai import types  # type: ignore

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_to_file import schema_write_file
from functions.run_python_file import schema_run_python_file


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
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
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


def call_function(function_call_part: object, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


def main():

    user_prompt, flags = _parse_args(sys.argv[1:])

    if not user_prompt:
        print("Please provide input text as a command-line argument.")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if "--verbose" in flags or "-v" in flags:
        print(
            f"""
              \nUser prompt: {user_prompt}
              \nPrompt tokens: {prompt_tokens}
              \nResponse tokens: {response_tokens}\n
            """
        )

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    if response.text:
        print(f"{response.text}")


if __name__ == "__main__":
    main()
