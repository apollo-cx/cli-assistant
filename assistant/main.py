import os
import sys
import json

from dotenv import load_dotenv  # type: ignore
from google import genai

# from openai import OpenAI
from google.genai import types  # type: ignore

from assistant.ui import (
    print_response,
    print_verbose_response,
    print_error,
    print_success,
    print_warning,
    print_request_info,
)

from assistant.functions.get_files_info import schema_get_files_info
from assistant.functions.get_file_content import schema_get_file_content
from assistant.functions.write_file_content import schema_write_file
from assistant.functions.run_python import schema_run_python

from assistant.argv_parser import parser
from assistant.call_function import call_function
from assistant.config import SYSTEM_PRPOMPT as system_prompt

load_dotenv()

# --- Neuro client setup ---
# api_key = os.environ.get("NEURO_API_KEY")
# base_url = os.environ.get("NEURO_BASE_URL")

# --- Gemini client setup ---
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- OpenAI client setup ---
# client = OpenAI(api_key=api_key, base_url=base_url)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)


def generate_response(client, messages, is_verbose=False, plain=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",  # qwen/qwen3-8b
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # Show request info in verbose mode
    if is_verbose:
        # Get the user prompt from the last message
        user_prompt = ""
        for msg in reversed(messages):
            if msg.role == "user":
                for part in msg.parts:
                    if part.text:
                        user_prompt = part.text
                        break
                if user_prompt:
                    break
        print_request_info(user_prompt, response, plain=plain)

    for candidate in response.candidates:
        messages.append(candidate.content)

    tool_responses = []

    if not response.function_calls and response.text:
        return response.text

    else:
        for function_call in response.function_calls:
            function_call_result = call_function(
                function_call, verbose=is_verbose, plain=plain
            )

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise RuntimeError("Function call did not return a function_response")

            tool_responses.append(function_call_result.parts[0])
            if is_verbose:
                response_data = function_call_result.parts[0].function_response.response
                print_verbose_response(response_data, plain=plain)

        messages.append(
            types.Content(
                role="user",
                parts=tool_responses,
            )
        )

    return None


def save_conversation(messages, filename="assistant/data/conversation_history.json"):
    """Save messages as JSON for later retrieval"""
    if not os.path.exists("assistant/data"):
        os.makedirs("assistant/data")

    # Convert messages to serializable format
    history = []
    for message in messages:
        msg_data = {"role": message.role}
        parts = []
        for part in message.parts:
            if part.text:
                parts.append({"type": "text", "text": part.text})
            elif part.function_response:
                parts.append(
                    {
                        "type": "function_response",
                        "name": part.function_response.name,
                        "response": dict(part.function_response.response),
                    }
                )
        msg_data["parts"] = parts
        history.append(msg_data)

    # Save history
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)


def get_saved_conversation(filename="assistant/data/conversation_history.json"):
    """Load previous messages as Content objects"""
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    # Convert back to Content objects
    messages = []
    for msg_data in history:
        parts = []
        for part_data in msg_data.get("parts", []):
            if part_data["type"] == "text":
                parts.append(types.Part(text=part_data["text"]))
            elif part_data["type"] == "function_response":
                parts.append(
                    types.Part.from_function_response(
                        name=part_data["name"], response=part_data["response"]
                    )
                )
        messages.append(types.Content(role=msg_data["role"], parts=parts))

    return messages


def clear_conversation_history(
    filename="assistant/data/conversation_history.json", plain=False
):
    if os.path.exists(filename):
        os.remove(filename)
        print_success("Conversation history cleared.", plain=plain)
    else:
        print_warning("No conversation history to clear.", plain=plain)


def main():
    args = parser.parse_args()
    user_prompt = " ".join(args.prompt)
    is_verbose = args.verbose
    is_clear_history = args.clear
    plain = args.plain

    if is_clear_history:
        clear_conversation_history(plain=plain)
        sys.exit

    if not user_prompt:
        print_error(
            "Please provide input text as a command-line argument.", plain=plain
        )
        sys.exit(1)

    old_messages = get_saved_conversation()

    messages = old_messages + [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        final_text = generate_response(client, messages, is_verbose, plain)
        if final_text:
            print_response(final_text, plain=plain)
            break

    save_conversation(messages)


if __name__ == "__main__":
    main()
