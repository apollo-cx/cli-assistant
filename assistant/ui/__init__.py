"""UI package for the CLI assistant with cyberpunk-styled interface.

This package provides a unified terminal UI with:
- Static cyberpunk ASCII borders
- Rich-formatted panels for messages
- Live display for smooth updates
- Markdown rendering for AI responses
"""

from .display import (
    print_banner,
    print_response,
    print_error,
    print_success,
    print_warning,
    print_verbose_response,
)
from .input import get_user_input_in_matrix
from .containers import matrix_container, processing_panel, function_calls_panel
from .legacy import (
    print_function_call,
    print_function_complete,
    print_code_block,
    print_request_info,
    print_divider,
    print_step,
)
from .config import console

__all__ = [
    # Display functions
    "print_banner",
    "print_response",
    "print_error",
    "print_success",
    "print_warning",
    "print_verbose_response",
    # Input functions
    "get_user_input_in_matrix",
    # Context managers
    "matrix_container",
    "processing_panel",
    "function_calls_panel",
    # Legacy functions
    "print_function_call",
    "print_function_complete",
    "print_code_block",
    "print_request_info",
    "print_divider",
    "print_step",
    # Console instance
    "console",
]
