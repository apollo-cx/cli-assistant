# UI Package

Cyberpunk-styled terminal UI package for the CLI assistant.

## Structure

```
ui/
├── __init__.py       # Package exports and public API
├── config.py         # Configuration constants and global state
├── layout.py         # Border generation and layout management
├── containers.py     # Context managers for display
├── display.py        # Main display functions
├── input.py          # User input handling
└── legacy.py         # Legacy/compatibility functions
```

## Module Overview

### `config.py`
- Configuration constants (colors, panel widths, message limits)
- Global state management (`console`, `_matrix_live`, `_matrix_center_content`)

### `layout.py`
- Border generation (`_create_cyberpunk_border`)
- Panel creation (`_create_side_panel`, `_create_center_panel`)
- Layout management (`_create_layout`, `_update_matrix_display`)

### `containers.py`
- `matrix_container()` - Main context manager for cyberpunk display
- `processing_panel()` - Animated spinner during AI processing
- `function_calls_panel()` - Display function execution

### `display.py`
- `print_banner()` - Startup banner
- `print_response()` - AI responses with markdown
- `print_error()`, `print_success()`, `print_warning()` - Status messages
- `print_verbose_response()` - Detailed response data

### `input.py`
- `get_user_input_in_matrix()` - User input with display pause/resume

### `legacy.py`
- Backward compatibility functions
- Token usage display
- Code block rendering
- Step-by-step process display

## Usage

```python
from assistant.ui import (
    matrix_container,
    print_banner,
    print_response,
    get_user_input_in_matrix,
)

# Use the cyberpunk display
with matrix_container():
    print_banner()
    print_response("Hello, world!")
    user_input = get_user_input_in_matrix("Prompt")
```

## Design

- **Static borders**: ASCII patterns (=, -, #) with gradient coloring
- **Three-column layout**: Fixed-width borders (22 cols) + flexible center
- **Live display**: Rich Live at 4 FPS for smooth updates
- **Message history**: Shows last 10 messages with scrolling
- **Markdown support**: AI responses rendered with Rich Markdown
