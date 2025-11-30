"""Main module for the CLI AI coding assistant.

This module provides the core functionality for interacting with a local LLM
(Qwen3) via OpenAI-compatible API. It supports tool calling for file operations,
conversation history management, and iterative AI-driven task execution.

The assistant can:
- List files and directories
- Read file contents
- Write/overwrite files
- Execute Python scripts

All operations are sandboxed to a specified working directory for security.
"""

import os
import sys
import json

from dotenv import load_dotenv  # type: ignore
from openai import OpenAI

from assistant.ui import (
    print_response,
    print_error,
    print_success,
    print_warning,
    print_banner,
    processing_panel,
    console,
)

from assistant.functions.function_schemas import (
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python,
)

from assistant.argv_parser import parser
from assistant.call_function import call_function
from assistant.config import SYSTEM_PROMPT

load_dotenv()

# --- Neuro client setup (Qwen3 LLM) ---
api_key = os.environ.get("NEURO_API_KEY")
base_url = os.environ.get("NEURO_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python,
]


def generate_response(client, messages, is_verbose=False):
    """Generate a response from the AI and execute any tool calls.

    Args:
        client: OpenAI client instance configured for the local LLM.
        messages: List of message dictionaries in OpenAI format.
        is_verbose: If True, print detailed function call information.

    Returns:
        The text content of the final response if no tool calls were made,
        or None if tool calls were executed (requiring another iteration).

    This function:
    1. Sends the current message history to the LLM
    2. Processes the response, handling both text and tool calls
    3. Executes any requested tool calls and appends results to messages
    4. Returns control for the next iteration or final output
    """
    # Show spinner while waiting for LLM response
    with processing_panel("AI is thinking"):
        response = client.chat.completions.create(
            model="qwen/qwen3-8b",
            messages=messages,
            tools=available_functions,
        )

    response_message = response.choices[0].message

    msg_dict = {"role": "assistant"}

    if response_message.content is not None:
        msg_dict["content"] = response_message.content

    if response_message.tool_calls:
        msg_dict["tool_calls"] = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in response_message.tool_calls
        ]

    messages.append(msg_dict)

    # If there are no tool calls, return the text response
    if not response_message.tool_calls:
        return response_message.content

    # Process tool calls
    for tool_call in response_message.tool_calls:
        function_result = call_function(tool_call, verbose=is_verbose)

        if is_verbose:
            print(f"-> {function_result}")

        # Add tool response to messages
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": json.dumps(function_result),
            }
        )

    return None


def save_conversation(messages, filename="assistant/data/conversation_history.json"):
    """Save conversation history to a JSON file.

    Args:
        messages: List of message dictionaries in OpenAI format.
        filename: Path to the JSON file where history will be saved.

    The conversation history allows the assistant to maintain context
    across multiple invocations, enabling multi-turn conversations.
    """
    if not os.path.exists("assistant/data"):
        os.makedirs("assistant/data")

    # All messages are already in dict format, just save them
    with open(filename, "w") as f:
        json.dump(messages, f, indent=2)


def get_saved_conversation(filename="assistant/data/conversation_history.json"):
    """Load conversation history from a JSON file.

    Args:
        filename: Path to the JSON file containing conversation history.

    Returns:
        List of message dictionaries in OpenAI format, or empty list
        if no history exists or the file cannot be parsed.
    """
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    # Messages are already in the correct format for OpenAI
    return history


def clear_conversation_history(filename="assistant/data/conversation_history.json"):
    """Delete the conversation history file.

    Args:
        filename: Path to the JSON file containing conversation history.

    This is useful for starting fresh conversations or clearing sensitive data.
    """
    if os.path.exists(filename):
        os.remove(filename)
        print_success("Conversation history cleared.")
    else:
        print_warning("No conversation history to clear.")


def main():
    """Main entry point for the CLI assistant.

    Handles:
    - Command-line argument parsing
    - Conversation history management
    - Message loop with the LLM (up to 20 iterations)
    - Tool execution via function calling
    - Final response output

    The assistant runs in an iterative loop, allowing the LLM to make
    multiple tool calls and process their results before generating
    a final response.
    """
    args = parser.parse_args()
    user_prompt = " ".join(args.prompt)
    is_verbose = args.verbose
    is_clear_history = args.clear

    if is_clear_history:
        clear_conversation_history()
        sys.exit

    if not user_prompt:
        print_error("Please provide input text as a command-line argument.")
        sys.exit(1)

    # Show beautiful banner
    print_banner()

    old_messages = get_saved_conversation()

    if not old_messages:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    else:
        messages = old_messages

    messages.append({"role": "user", "content": user_prompt})

    for _ in range(20):
        final_text = generate_response(client, messages, is_verbose)
        if final_text:
            print_response(final_text)
            break

    save_conversation(messages)


if __name__ == "__main__":
    main()
