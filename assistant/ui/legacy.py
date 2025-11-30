"""Legacy display functions for backward compatibility."""

from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich import box

from .config import (
    console,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
)


def print_function_call(function_name, args):
    """Format function call notification.

    Args:
        function_name: Name of function being called
        args: Function arguments

    Returns:
        Formatted string
    """
    return f"[bold {COLOR_PRIMARY}]>[/bold {COLOR_PRIMARY}] [{COLOR_SECONDARY}]{function_name}[/{COLOR_SECONDARY}] [dim {COLOR_SECONDARY}]{args}[/dim {COLOR_SECONDARY}]"


def print_function_complete(function_name):
    """Display function completion.

    Args:
        function_name: Name of completed function
    """
    console.print(
        f"[bold {COLOR_SUCCESS}]+[/bold {COLOR_SUCCESS}] [{COLOR_SECONDARY}]{function_name}[/{COLOR_SECONDARY}] [{COLOR_SUCCESS}]completed[/{COLOR_SUCCESS}]"
    )


def print_code_block(code, language="python"):
    """Display code block with syntax highlighting.

    Args:
        code: Source code to display
        language: Programming language
    """
    markdown_code = f"```{language}\n{code}\n```"
    console.print(
        Panel(
            Markdown(markdown_code),
            border_style=f"dim {COLOR_PRIMARY}",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def print_request_info(user_prompt, response=None):
    """Display request information and token usage.

    Args:
        user_prompt: User's input prompt
        response: API response with metadata
    """
    from rich.table import Table

    table = Table(
        title=f"[bold {COLOR_SECONDARY}]Request Information[/bold {COLOR_SECONDARY}]",
        border_style=COLOR_PRIMARY,
        box=box.ROUNDED,
        show_header=True,
        header_style=f"bold {COLOR_SECONDARY}",
        row_styles=["dim", ""],
    )
    table.add_column("Property", style=COLOR_SECONDARY, no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row(
        "User Prompt",
        user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
    )

    if response and hasattr(response, "usage_metadata"):
        try:
            metadata = response.usage_metadata
            table.add_row("Prompt Tokens", str(metadata.prompt_token_count))
            table.add_row("Response Tokens", str(metadata.candidates_token_count))
            table.add_row("Total Tokens", str(metadata.total_token_count))
        except Exception:
            pass

    console.print()
    console.print(table)
    console.print()


def print_divider(text=""):
    """Print visual divider.

    Args:
        text: Optional divider text
    """
    if text:
        console.print()
        console.print(
            Panel(
                Text(text, style=f"bold {COLOR_SECONDARY}", justify="center"),
                border_style=COLOR_PRIMARY,
                box=box.ROUNDED,
                padding=(0, 1),
            )
        )
        console.print()
    else:
        console.print(
            f"[dim {COLOR_SECONDARY}]" + "─" * 60 + f"[/dim {COLOR_SECONDARY}]"
        )


def print_step(step_num, total_steps, message):
    """Display numbered step in multi-step process.

    Args:
        step_num: Current step number
        total_steps: Total number of steps
        message: Step description
    """
    console.print(
        f"[bold {COLOR_PRIMARY}][{step_num}[/bold {COLOR_PRIMARY}][dim]/{total_steps}[/dim][bold {COLOR_PRIMARY}]][/bold {COLOR_PRIMARY}] "
        f"[{COLOR_SECONDARY}]{message}[/{COLOR_SECONDARY}]"
    )
