"""Display functions for output."""

from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.align import Align
from rich import box

from .config import (
    console,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ERROR,
    COLOR_SUCCESS,
    COLOR_WARNING,
)
from .containers import _add_to_matrix_or_print


def print_banner():
    """Display startup banner."""
    banner_text = Text()
    banner_text.append("   _____ _      _____ \n", style=f"bold {COLOR_SECONDARY}")
    banner_text.append("  / ____| |    |_   _|\n", style=f"bold {COLOR_SECONDARY}")
    banner_text.append(" | |    | |      | |  \n", style=COLOR_SECONDARY)
    banner_text.append(" | |    | |      | |  \n", style=COLOR_SECONDARY)
    banner_text.append(" | |____| |____ _| |_ \n", style=COLOR_SECONDARY)
    banner_text.append("  \\_____|______|_____|\n", style=COLOR_SECONDARY)
    banner_text.append("\n   AI Assistant\n", style=f"bold {COLOR_SECONDARY}")
    banner_text.append("   Powered by Qwen3-8b", style=f"dim {COLOR_SECONDARY}")

    panel = Panel(
        banner_text,
        title="[bold magenta]Welcome[/bold magenta]",
        title_align="left",
        border_style=COLOR_PRIMARY,
        box=box.ROUNDED,
        padding=(0, 1),
    )
    _add_to_matrix_or_print(panel)


def print_response(text):
    """Display AI response with markdown rendering.

    Args:
        text: Response text (markdown supported)
    """
    panel = Panel(
        Markdown(text),
        title="[bold cyan]AI Response[/bold cyan]",
        title_align="left",
        border_style=COLOR_PRIMARY,
        box=box.ROUNDED,
        padding=(0, 1),
    )
    _add_to_matrix_or_print(panel)


def print_error(message):
    """Display error message.

    Args:
        message: Error message text
    """
    console.print(
        f"[bold {COLOR_ERROR}]X[/bold {COLOR_ERROR}] [{COLOR_ERROR}]{message}[/{COLOR_ERROR}]"
    )


def print_success(message):
    """Display success message.

    Args:
        message: Success message text
    """
    console.print(
        f"[bold {COLOR_SUCCESS}]+[/bold {COLOR_SUCCESS}] [{COLOR_SUCCESS}]{message}[/{COLOR_SUCCESS}]"
    )


def print_warning(message):
    """Display warning message.

    Args:
        message: Warning message text
    """
    console.print(
        f"[bold {COLOR_WARNING}]![/bold {COLOR_WARNING}] [{COLOR_WARNING}]{message}[/{COLOR_WARNING}]"
    )


def print_verbose_response(response_data):
    """Display detailed response data.

    Args:
        response_data: Full response object
    """
    console.print(
        Panel(
            Align.center(str(response_data)),
            title=f"[bold {COLOR_SECONDARY}]Response[/bold {COLOR_SECONDARY}]",
            border_style=COLOR_PRIMARY,
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )
