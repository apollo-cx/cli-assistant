"""UI utilities for rich formatting.

This module provides a unified interface for terminal output with rich
formatting including colors, panels, spinners, and markdown rendering.

Rich Library Features Used:
- Console: Main output handler with color and style support
- Panel: Bordered containers with titles for organized content display
- Markdown: Renders markdown text with syntax highlighting
- Table: Creates formatted tables with customizable columns and styling
- Status: Context manager for animated spinners during operations
- Text: Styled text with gradient support
- Box: Custom box styles for panels (ROUNDED, DOUBLE, HEAVY, etc.)

Important Notes:
- Animations (spinners) only appear in interactive terminals
- Rich automatically disables animations when output is piped/redirected
- Spinners disappear when operations complete (this is normal behavior)
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text
from rich import box
from rich.style import Style
from rich.live import Live
from rich.spinner import Spinner
from rich.align import Align
from contextlib import contextmanager

# Global console instance for all rich output operations
# force_terminal=True would force colors even when piped, but we use auto-detection
console = Console()


@contextmanager
def processing_panel(message="AI is thinking"):
    """Context manager for displaying a processing panel with animated spinner.

    Args:
        message: Message to display in the spinner.

    Yields:
        None

    Example:
        with processing_panel("AI is thinking"):
            # Do some processing
            result = some_function()
    """
    spinner_text = Text()
    spinner_text.append(message, style="bold cyan")
    spinner_text.append("...", style="cyan")
    spinner_text.justify = "center"

    spinner = Spinner("aesthetic", text=spinner_text, style="magenta")

    # Create a centered renderable
    centered_spinner = Align.center(spinner)

    panel = Panel(
        centered_spinner,
        title="[bold cyan]Processing Request[/bold cyan]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(0, 1),
    )

    console.print()
    with Live(panel, console=console, refresh_per_second=10):
        yield
    console.print()


def print_function_call(function_name, args):
    """Display a function call notification with formatting.

    Args:
        function_name: Name of the function being called.
        args: Dictionary of arguments passed to the function.

    Returns:
        Formatted string for use with console.status() spinner.

    Rich Features:
        - Magenta highlight
        - Cyan for function name
        - Dim cyan for arguments
        - Used with console.status() to show animated spinner

    Example:
        spinner_text = print_function_call("get_file", {"path": "test.py"})
        with console.status(spinner_text, spinner="dots"):
            # Execute function
            pass
    """
    return f"[bold magenta]>[/bold magenta] [cyan]{function_name}[/cyan] [dim cyan]{args}[/dim cyan]"


def print_function_complete(function_name):
    """Display function completion notification.

    Args:
        function_name: Name of the completed function.

    Rich Features:
        - Green check mark
        - Cyan for function name
        - console.print() for rich text rendering

    Example:
        print_function_complete("get_file")
        # Output: + get_file completed (in vibrant colors)
    """
    console.print(
        f"[bold green]+[/bold green] [cyan]{function_name}[/cyan] [green]completed[/green]"
    )


def print_response(text):
    """Display the AI's response with formatting.

    Args:
        text: The response text to display (supports markdown).

    Rich Features:
        - Panel: Creates a rounded bordered box with beautiful styling
        - Markdown: Renders markdown syntax (headers, code blocks, lists, etc.)
        - Magenta border with cyan title for visual appeal
        - Extra padding for breathing room
        - Centered text

    Example:
        response = "Here's some **bold** text and `code`"
        print_response(response)
        # Displays a stunning rounded panel with rendered markdown
    """
    # Create centered text instead of markdown for better centering
    from rich.text import Text as RichText

    centered_text = RichText(text, justify="center")

    console.print()
    console.print(
        Panel(
            centered_text,
            title="[bold cyan]AI Response[/bold cyan]",
            border_style="magenta",
            box=box.ROUNDED,
            padding=(1, 3),
        )
    )
    console.print()


def print_verbose_response(response_data):
    """Display detailed function response data in verbose mode.

    Args:
        response_data: The response data to display.

    Rich Features:
        - Panel: Rounded bordered container for organized display
        - Magenta border with cyan title
        - Double box style for emphasis

    Example:
        data = {"result": "File contents..."}
        print_verbose_response(data)
        # Displays beautiful magenta-bordered panel with the data
    """
    console.print(
        Panel(
            Align.center(str(response_data)),
            title="[bold cyan]Response[/bold cyan]",
            border_style="magenta",
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )


def print_error(message):
    """Display an error message with formatting.

    Args:
        message: Error message to display.

    Rich Features:
        - Bold red X for high visibility
        - Red text for immediate attention
        - console.print() for styled output

    Example:
        print_error("File not found")
        # Output: X File not found (in bold red)
    """
    console.print(f"[bold red]X[/bold red] [red]{message}[/red]")


def print_success(message):
    """Display a success message with formatting.

    Args:
        message: Success message to display.

    Rich Features:
        - Bold green check mark
        - Green text for positive reinforcement
        - console.print() for styled output

    Example:
        print_success("File saved successfully")
        # Output: + File saved successfully (in vibrant green)
    """
    console.print(f"[bold green]+[/bold green] [green]{message}[/green]")


def print_warning(message):
    """Display a warning message with formatting.

    Args:
        message: Warning message to display.

    Rich Features:
        - Bold yellow warning symbol
        - Bright yellow text for attention-grabbing
        - console.print() for styled output

    Example:
        print_warning("Large file may be truncated")
        # Output: ! Large file may be truncated (in bold yellow)
    """
    console.print(f"[bold yellow]![/bold yellow]  [yellow]{message}[/yellow]")


def print_request_info(user_prompt, response=None):
    """Display detailed request information including token usage.

    Args:
        user_prompt: The user's input prompt.
        response: Optional response object containing usage metadata.

    Rich Features:
        - Table: Beautiful multi-column table with rounded borders
        - Magenta border with cyan text
        - Color-coded columns
        - Row highlighting for better readability

    Example:
        print_request_info("Analyze this code", response_obj)
        # Displays a stunning table with prompt and token counts

    Note:
        Token usage extraction attempts to read 'usage_metadata' attribute
        from the response object. Gracefully handles missing attributes.
    """
    table = Table(
        title="[bold cyan]Request Information[/bold cyan]",
        border_style="magenta",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        row_styles=["dim", ""],
    )
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row(
        "User Prompt",
        user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
    )

    if response:
        try:
            if hasattr(response, "usage_metadata"):
                metadata = response.usage_metadata
                table.add_row("Prompt Tokens", str(metadata.prompt_token_count))
                table.add_row("Response Tokens", str(metadata.candidates_token_count))
                table.add_row("Total Tokens", str(metadata.total_token_count))
        except:
            pass

    console.print()
    console.print(table)
    console.print()


def print_banner():
    """Display a beautiful startup banner.

    Rich Features:
        - ASCII art banner with cyan coloring
        - Rounded panel with magenta border
        - Welcome message

    Example:
        print_banner()
        # Displays a colorful welcome banner
    """
    banner_text = Text()
    banner_text.append("   _____ _      _____ \n", style="bold cyan")
    banner_text.append("  / ____| |    |_   _|\n", style="bold cyan")
    banner_text.append(" | |    | |      | |  \n", style="cyan")
    banner_text.append(" | |    | |      | |  \n", style="cyan")
    banner_text.append(" | |____| |____ _| |_ \n", style="cyan")
    banner_text.append("  \\_____|______|_____|\n", style="cyan")
    banner_text.append("\n   ", style="")
    banner_text.append("AI Assistant", style="bold cyan")
    banner_text.append("\n", style="")
    banner_text.append("   Powered by ", style="dim")
    banner_text.append("Qwen3-8b", style="bold cyan")

    console.print()
    console.print(
        Panel(
            Align.center(banner_text),
            border_style="magenta",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()


def print_divider(text=""):
    """Print a visual divider with optional text.

    Args:
        text: Optional text to display in the divider.

    Rich Features:
        - Panel with centered text and magenta border
        - Minimal padding for clean look

    Example:
        print_divider("Processing")
        # Displays a styled panel with "Processing" centered
    """
    if text:
        console.print()
        console.print(
            Panel(
                Text(text, style="bold cyan", justify="center"),
                border_style="magenta",
                box=box.ROUNDED,
                padding=(0, 1),
            )
        )
        console.print()
    else:
        console.print("[dim cyan]" + "─" * 60 + "[/dim cyan]")


def print_processing_panel():
    """Display a processing panel with centered loading indicator.

    Rich Features:
        - Panel with "Processing Request" title
        - Centered loading indicator
        - Magenta border for consistency

    Example:
        print_processing_panel()
        # Displays a panel with loading bar
    """
    loading_text = Text()
    loading_text.append("●", style="bold magenta")
    loading_text.append(" ", style="")
    loading_text.append("●", style="bold cyan")
    loading_text.append(" ", style="")
    loading_text.append("●", style="bold magenta")

    console.print()
    console.print(
        Panel(
            Align.center(loading_text),
            title="[bold cyan]Processing Request[/bold cyan]",
            border_style="magenta",
            box=box.ROUNDED,
            padding=(0, 1),
        )
    )
    console.print()


def print_step(step_num, total_steps, message):
    """Display a numbered step in a multi-step process.

    Args:
        step_num: Current step number.
        total_steps: Total number of steps.
        message: Description of the current step.

    Rich Features:
        - Magenta numbered badge
        - Progress indicator with colors
        - Visual step counter

    Example:
        print_step(1, 3, "Loading files")
        # Displays: [1/3] Loading files (with beautiful styling)
    """
    console.print(
        f"[bold magenta][{step_num}[/bold magenta][dim]/{total_steps}[/dim][bold magenta]][/bold magenta] "
        f"[cyan]{message}[/cyan]"
    )


def print_code_block(code, language="python"):
    """Display a code block with syntax highlighting.

    Args:
        code: The code to display.
        language: Programming language for syntax highlighting.

    Rich Features:
        - Syntax highlighting via Markdown
        - Magenta-themed code panel
        - Rounded borders

    Example:
        print_code_block("def hello():\\n    print('hi')", "python")
        # Displays a beautifully highlighted code block
    """
    markdown_code = f"```{language}\n{code}\n```"
    console.print(
        Panel(
            Markdown(markdown_code),
            border_style="dim magenta",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
