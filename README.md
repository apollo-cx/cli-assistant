# CLI AI Coding Assistant

A command-line AI coding assistant powered by local LLM (Qwen3) via OpenAI-compatible API. The assistant can interact with your filesystem, execute Python scripts, and maintain conversation history across sessions.

## Features

- 🤖 **Local LLM Integration**: Uses Qwen3 via OpenAI-compatible API (Neuro/Ollama)
- 📁 **File Operations**: List, read, and write files within a sandboxed directory
- 🐍 **Python Execution**: Run Python scripts with argument support
- 💬 **Conversation History**: Maintains context across multiple invocations
- 🔒 **Security Sandboxing**: All operations restricted to a configured working directory
- 🛠️ **Tool Calling**: Leverages OpenAI function calling for structured operations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/apollo-cx/cli-assistant.git
cd cli-assistant
```

2. Install dependencies:
```bash
pip install -e .
```

3. Create a `.env` file in the `assistant/` directory:
```env
NEURO_API_KEY=your_api_key_here
NEURO_BASE_URL=http://localhost:11434/v1  # Or your LLM server URL
```

## Usage

### Basic Commands

Ask the AI assistant a question:
```bash
ai "what files are in this directory?"
```

Get verbose output showing function calls:
```bash
ai -v "read the main.py file"
```

Clear conversation history:
```bash
ai --clear
```

### Examples

List all Python files:
```bash
ai "list all .py files in the current directory"
```

Read and analyze code:
```bash
ai "read main.py and explain what it does"
```

Write a new file:
```bash
ai "create a hello.py file that prints 'Hello, World!'"
```

Execute a Python script:
```bash
ai "run the test.py file"
```

Multi-step operations:
```bash
ai "read utils.py, find bugs, and fix them"
```

## Configuration

Edit `assistant/config.py` to customize:

- `MAX_CHARS`: Maximum file size to read (default: 10,000 characters)
- `WORKING_DIR`: Directory where operations are allowed (default: `./calculator`)
- `ITERATION_LIMIT`: Max conversation iterations per query (default: 20)
- `SYSTEM_PROMPT`: AI assistant's behavior and instructions

## Project Structure

```
cli-assistant/
├── assistant/
│   ├── __init__.py
│   ├── main.py                 # Main entry point and conversation loop
│   ├── argv_parser.py          # Command-line argument definitions
│   ├── call_function.py        # Function call dispatcher
│   ├── config.py               # Configuration settings
│   ├── data/
│   │   └── conversation_history.json  # Saved conversations
│   └── functions/
│       ├── __init__.py
│       ├── function_schemas.py # OpenAI tool schemas
│       ├── get_file_content.py # File reading function
│       ├── get_files_info.py   # Directory listing function
│       ├── run_python.py       # Python execution function
│       └── write_file_content.py # File writing function
├── pyproject.toml
└── README.md
```

## How It Works

1. **User Input**: You provide a natural language prompt via the CLI
2. **LLM Processing**: The prompt is sent to your local LLM (Qwen3)
3. **Tool Calling**: The LLM can request function calls (read file, list dir, etc.)
4. **Function Execution**: Requested functions are executed and results returned
5. **Iteration**: Steps 2-4 repeat up to 20 times until a final answer is generated
6. **History Saved**: The conversation is saved for context in future interactions

## Available Functions

The AI can use the following tools:

### `get_files_info`
Lists files and directories with sizes and types.
- **Parameter**: `directory` (optional) - subdirectory to list

### `get_file_content`
Reads file contents (truncated at MAX_CHARS).
- **Parameter**: `file_path` (required) - path to file

### `write_file`
Writes or overwrites a file.
- **Parameters**: 
  - `file_path` (required) - path to file
  - `content` (required) - content to write

### `run_python`
Executes a Python script with 30-second timeout.
- **Parameter**: `file_path` (required) - path to Python file

## Security Features

- **Directory Sandboxing**: All operations are restricted to `WORKING_DIR`
- **Path Validation**: Absolute path checks prevent directory traversal attacks
- **File Size Limits**: Large files are truncated to prevent memory issues
- **Execution Timeout**: Python scripts timeout after 30 seconds
- **Error Handling**: All functions return error messages instead of raising exceptions

## Requirements

- Python 3.8+
- OpenAI Python SDK
- python-dotenv
- A local LLM server with OpenAI-compatible API (e.g., Ollama, LM Studio)

## Command-Line Options

```
usage: ai [-h] [-c] [-v] [-s] [prompt ...]

AI Coding Agent - Local LLM-powered coding assistant

positional arguments:
  prompt         User prompt for the AI agent

options:
  -h, --help     show this help message and exit
  -c, --clear    Clear conversation history
  -v, --verbose  Enable verbose output
  -s, --silent   Enable silent mode
```

## Development

### Running Tests
```bash
python -m pytest assistant/tests.py
```

### Adding New Functions

1. Create function implementation in `assistant/functions/`
2. Add schema to `assistant/functions/function_schemas.py`
3. Register in `call_function.py` function map
4. Import schema in `main.py`

## Troubleshooting

**Error: "Cannot connect to LLM"**
- Check that your local LLM server is running
- Verify `NEURO_BASE_URL` in `.env` is correct

**Error: "Outside permitted directory"**
- All operations must be within `WORKING_DIR`
- Update `WORKING_DIR` in `config.py` if needed

**Assistant not remembering context**
- Conversation history is saved in `assistant/data/conversation_history.json`
- Use `ai --clear` to reset if history becomes corrupted

## Acknowledgments

- Built with [OpenAI Python SDK](https://github.com/openai/openai-python)
- Designed for local LLM deployment (Qwen3, Ollama, etc.)

(This file was generated by the cli-assistant)
