"""
OpenAI function schemas for tool calling.

Defines the JSON schemas that describe available functions to the LLM.
These schemas follow the OpenAI function calling format and specify:
- Function names
- Descriptions of what each function does
- Parameter definitions with types and descriptions
- Required vs optional parameters

The LLM uses these schemas to understand which functions are available
and how to format the arguments when making function calls.
"""

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                }
            },
        },
    },
}

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a specified file and truncates it if it is over MAX_CHARS (variable) bytes large, limited to working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory.",
                }
            },
            "required": ["file_path"],
        },
    },
}

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites content to a specified file within the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write to, relative to the working directory. If not provided, writes to the working directory itself.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

schema_run_python = {
    "type": "function",
    "function": {
        "name": "run_python",
        "description": "Executes a specified Python file with optional arguments, limited to working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory.",
                }
            },
            "required": ["file_path"],
        },
    },
}
