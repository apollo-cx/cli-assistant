"""UI utilities for rich formatting with matrix rain animation.

This module provides a unified interface for terminal output with rich
formatting including colors, panels, spinners, and animated matrix rain effects.
"""

from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text
from rich import box
from rich.live import Live
from rich.spinner import Spinner
from rich.align import Align
from rich.layout import Layout
from contextlib import contextmanager
import random
import time
import threading

# =============================================================================
# CONSTANTS
# =============================================================================

MATRIX_CHARS = "01アイウエオカキクケコサシスセソタチツテト"
MATRIX_PANEL_WIDTH = 12
MATRIX_REFRESH_RATE = 12  # FPS
MATRIX_ANIMATION_DELAY = 0.08  # seconds

COLOR_PRIMARY = "magenta"
COLOR_SECONDARY = "cyan"
COLOR_SUCCESS = "green"
COLOR_ERROR = "red"
COLOR_WARNING = "yellow"
COLOR_MATRIX = "green"

# =============================================================================
# GLOBALS
# =============================================================================

console = Console()

# Matrix animation state
_matrix_live = None
_matrix_center_content = []
_matrix_columns = {}
_matrix_stop_event = threading.Event()

# =============================================================================
# MATRIX ANIMATION
# =============================================================================


class MatrixColumn:
    """A single column of falling matrix characters with waterfall effect."""

    def __init__(self, width=6):
        self.width = width
        self.offset = random.randint(0, 10)

    def generate(self, height):
        """Generate the matrix column with scrolling waterfall effect."""
        self.offset = (self.offset + 1) % height
        text = Text()

        for i in range(height):
            pos = (i + self.offset) % height
            line = "".join(random.choice(MATRIX_CHARS) for _ in range(self.width))

            # Brightness gradient: bright at top, dim at bottom
            if pos < 3:
                style = "bold bright_green"
            elif pos < 7:
                style = COLOR_MATRIX
            else:
                style = f"dim {COLOR_MATRIX}"

            text.append(line + "\n", style=style)

        return text


def _get_terminal_height():
    """Get the current terminal height with fallback."""
    try:
        return max(console.size.height - 4, 20)
    except:
        return 30


def _create_matrix_panel(matrix_column, height):
    """Create a panel for a matrix column."""
    return Panel(
        matrix_column.generate(height),
        border_style=f"dim {COLOR_MATRIX}",
        box=box.ROUNDED,
        padding=(0, 1),
    )


def _create_center_panel(content_list):
    """Create the center content panel."""
    content = Group(*content_list) if content_list else Text("")
    return Panel(
        content,
        border_style=f"bold {COLOR_PRIMARY}",
        box=box.HEAVY,
        padding=(1, 2),
    )


def _create_layout(left_panel, center_panel, right_panel):
    """Create the three-column layout with fixed matrix widths."""
    layout = Layout()
    layout.split_row(
        Layout(left_panel, size=MATRIX_PANEL_WIDTH),
        Layout(center_panel, ratio=1),
        Layout(right_panel, size=MATRIX_PANEL_WIDTH),
    )
    return layout


def _update_matrix_display():
    """Update the matrix display with current center content."""
    global _matrix_live, _matrix_center_content, _matrix_columns

    if _matrix_live is None:
        return

    # Initialize matrix columns if needed
    if "left" not in _matrix_columns:
        _matrix_columns["left"] = MatrixColumn(width=6)
    if "right" not in _matrix_columns:
        _matrix_columns["right"] = MatrixColumn(width=6)

    height = _get_terminal_height()

    # Create all three panels
    left_panel = _create_matrix_panel(_matrix_columns["left"], height)
    center_panel = _create_center_panel(_matrix_center_content)
    right_panel = _create_matrix_panel(_matrix_columns["right"], height)

    # Update the live display
    layout = _create_layout(left_panel, center_panel, right_panel)
    _matrix_live.update(layout)


def _matrix_animation_loop():
    """Continuously update matrix rain animation."""
    while not _matrix_stop_event.is_set():
        _update_matrix_display()
        time.sleep(MATRIX_ANIMATION_DELAY)


@contextmanager
def matrix_container():
    """Context manager for displaying content with animated matrix rain.

    Example:
        with matrix_container():
            print_banner()
            print_response("Hello")
    """
    global _matrix_live, _matrix_center_content, _matrix_columns, _matrix_stop_event

    # Reset state
    _matrix_center_content.clear()
    _matrix_columns.clear()
    _matrix_stop_event.clear()

    console.print()

    # Start live display
    _matrix_live = Live(
        console=console,
        refresh_per_second=MATRIX_REFRESH_RATE,
        auto_refresh=False
    )
    _matrix_live.start()
    _update_matrix_display()

    # Start animation thread
    animation_thread = threading.Thread(target=_matrix_animation_loop, daemon=True)
    animation_thread.start()

    try:
        yield
    finally:
        # Stop animation
        _matrix_stop_event.set()
        animation_thread.join(timeout=0.5)
        time.sleep(1.5)

        # Stop live display
        _matrix_live.stop()
        _matrix_live = None
        console.print()


def _add_to_matrix_or_print(panel):
    """Add panel to matrix container if active, otherwise print directly."""
    if _matrix_live is not None:
        _matrix_center_content.append(panel)
        _update_matrix_display()
    else:
        console.print()
        console.print(panel)
        console.print()


# =============================================================================
# CONTEXT MANAGERS
# =============================================================================


@contextmanager
def processing_panel(message="AI is thinking"):
    """Display a processing panel with animated spinner.

    Args:
        message: Message to display in the spinner.
    """
    global _matrix_live, _matrix_center_content

    spinner_text = Text()
    spinner_text.append(message, style=f"bold {COLOR_SECONDARY}")
    spinner_text.append("...", style=COLOR_SECONDARY)
    spinner_text.justify = "center"

    panel = Panel(
        Align.center(Spinner("aesthetic", text=spinner_text, style=COLOR_PRIMARY)),
        title=f"[bold {COLOR_SECONDARY}]Processing Request[/bold {COLOR_SECONDARY}]",
        border_style=COLOR_PRIMARY,
        box=box.ROUNDED,
        padding=(0, 1),
    )

    if _matrix_live is not None:
        _matrix_center_content.append(panel)
        try:
            yield
        finally:
            if panel in _matrix_center_content:
                _matrix_center_content.remove(panel)
            _update_matrix_display()
    else:
        console.print()
        with Live(panel, console=console, refresh_per_second=10):
            yield
        console.print()


@contextmanager
def function_calls_panel():
    """Context manager for displaying function calls in a panel."""
    global _matrix_live, _matrix_center_content

    renderables = []
    yield renderables

    if renderables:
        panel = Panel(
            Align.center(Group(*renderables)),
            title=f"[bold {COLOR_SECONDARY}]Calling Function[/bold {COLOR_SECONDARY}]",
            border_style=COLOR_PRIMARY,
            box=box.ROUNDED,
            padding=(0, 1),
        )

        if _matrix_live is not None:
            _matrix_center_content.append(panel)
            _update_matrix_display()
        else:
            console.print()
            console.print(panel)


# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================


def print_banner():
    """Display the startup banner."""
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
        Align.center(banner_text),
        border_style=COLOR_PRIMARY,
        box=box.ROUNDED,
        padding=(1, 2),
    )
    _add_to_matrix_or_print(panel)


def print_response(text):
    """Display the AI's response."""
    panel = Panel(
        Text(text, justify="center"),
        title=f"[bold {COLOR_SECONDARY}]AI Response[/bold {COLOR_SECONDARY}]",
        border_style=COLOR_PRIMARY,
        box=box.ROUNDED,
        padding=(1, 3),
    )
    _add_to_matrix_or_print(panel)


def print_error(message):
    """Display an error message."""
    console.print(f"[bold {COLOR_ERROR}]X[/bold {COLOR_ERROR}] [{COLOR_ERROR}]{message}[/{COLOR_ERROR}]")


def print_success(message):
    """Display a success message."""
    console.print(f"[bold {COLOR_SUCCESS}]+[/bold {COLOR_SUCCESS}] [{COLOR_SUCCESS}]{message}[/{COLOR_SUCCESS}]")


def print_warning(message):
    """Display a warning message."""
    console.print(f"[bold {COLOR_WARNING}]![/bold {COLOR_WARNING}] [{COLOR_WARNING}]{message}[/{COLOR_WARNING}]")


def print_verbose_response(response_data):
    """Display detailed response data in verbose mode."""
    console.print(
        Panel(
            Align.center(str(response_data)),
            title=f"[bold {COLOR_SECONDARY}]Response[/bold {COLOR_SECONDARY}]",
            border_style=COLOR_PRIMARY,
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )


# =============================================================================
# USER INPUT
# =============================================================================


def get_user_input_in_matrix(prompt_text="You"):
    """Get user input within the matrix container."""
    global _matrix_live, _matrix_center_content, _matrix_stop_event, _matrix_columns

    # Stop animation
    if _matrix_live is not None:
        _matrix_live.stop()
        _matrix_stop_event.set()

    # Display current state with static matrix
    height = _get_terminal_height()
    
    left_matrix = Panel(
        Text("\n".join("".join(random.choice(MATRIX_CHARS) for _ in range(6)) 
                       for _ in range(height)), style=COLOR_MATRIX),
        border_style=f"dim {COLOR_MATRIX}",
        box=box.ROUNDED,
        padding=(0, 1),
    )
    
    right_matrix = Panel(
        Text("\n".join("".join(random.choice(MATRIX_CHARS) for _ in range(6)) 
                       for _ in range(height)), style=COLOR_MATRIX),
        border_style=f"dim {COLOR_MATRIX}",
        box=box.ROUNDED,
        padding=(0, 1),
    )

    center_panel = _create_center_panel(_matrix_center_content)
    layout = _create_layout(left_matrix, center_panel, right_matrix)

    console.clear()
    console.print(layout)
    console.print()

    # Get input
    console.print(f"[bold {COLOR_PRIMARY}]You:[/bold {COLOR_PRIMARY}] ", end="")
    try:
        user_input = input()
    except EOFError:
        user_input = ""

    # Add user message to content
    if user_input.strip():
        panel = Panel(
            Align.center(Text(user_input, style="white")),
            title=f"[bold {COLOR_SECONDARY}]User Message[/bold {COLOR_SECONDARY}]",
            border_style=COLOR_PRIMARY,
            box=box.ROUNDED,
            padding=(0, 2),
        )
        _matrix_center_content.append(panel)

    # Restart animation
    if _matrix_live is not None:
        _matrix_stop_event.clear()
        _matrix_columns.clear()
        _matrix_live.start()
        
        animation_thread = threading.Thread(target=_matrix_animation_loop, daemon=True)
        animation_thread.start()
        _update_matrix_display()

    return user_input


# =============================================================================
# LEGACY/UNUSED FUNCTIONS (kept for compatibility)
# =============================================================================


def print_function_call(function_name, args):
    """Display a function call notification."""
    return f"[bold {COLOR_PRIMARY}]>[/bold {COLOR_PRIMARY}] [{COLOR_SECONDARY}]{function_name}[/{COLOR_SECONDARY}] [dim {COLOR_SECONDARY}]{args}[/dim {COLOR_SECONDARY}]"


def print_function_complete(function_name):
    """Display function completion notification."""
    console.print(
        f"[bold {COLOR_SUCCESS}]+[/bold {COLOR_SUCCESS}] [{COLOR_SECONDARY}]{function_name}[/{COLOR_SECONDARY}] [{COLOR_SUCCESS}]completed[/{COLOR_SUCCESS}]"
    )


def print_code_block(code, language="python"):
    """Display a code block with syntax highlighting."""
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
    """Display detailed request information including token usage."""
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
        except:
            pass

    console.print()
    console.print(table)
    console.print()


def print_divider(text=""):
    """Print a visual divider with optional text."""
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
        console.print(f"[dim {COLOR_SECONDARY}]" + "─" * 60 + f"[/dim {COLOR_SECONDARY}]")


def print_step(step_num, total_steps, message):
    """Display a numbered step in a multi-step process."""
    console.print(
        f"[bold {COLOR_PRIMARY}][{step_num}[/bold {COLOR_PRIMARY}][dim]/{total_steps}[/dim][bold {COLOR_PRIMARY}]][/bold {COLOR_PRIMARY}] "
        f"[{COLOR_SECONDARY}]{message}[/{COLOR_SECONDARY}]"
    )
