"""Context managers for display management."""

from contextlib import contextmanager
import time
import threading

from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich import box

from .config import (
    console,
    _matrix_live,
    _matrix_center_content,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
)
from .layout import _update_matrix_display


@contextmanager
def matrix_container():
    """Context manager for cyberpunk-styled display.

    Yields control to caller while maintaining Live display.

    Example:
        with matrix_container():
            print_banner()
            print_response("Hello")
    """
    import assistant.ui.config as config

    config._matrix_center_content.clear()
    console.print()

    config._matrix_live = Live(console=console, refresh_per_second=4, auto_refresh=True)
    config._matrix_live.start()
    _update_matrix_display()

    try:
        yield
    finally:
        time.sleep(1.5)
        config._matrix_live.stop()
        config._matrix_live = None
        console.print()


def _add_to_matrix_or_print(panel):
    """Add panel to matrix display or print directly.

    Args:
        panel: Rich renderable to display
    """
    import assistant.ui.config as config

    if config._matrix_live is not None:
        config._matrix_center_content.append(panel)
        _update_matrix_display()
    else:
        console.print()
        console.print(panel)
        console.print()


@contextmanager
def processing_panel(message="AI is thinking"):
    """Display processing spinner during AI operations.

    Args:
        message: Status message to display
    """
    import assistant.ui.config as config
    import threading

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

    if config._matrix_live is not None:
        config._matrix_center_content.append(panel)

        # Start animation thread to keep spinner moving
        stop_event = threading.Event()

        def animate_spinner():
            while not stop_event.is_set():
                _update_matrix_display()
                time.sleep(0.08)  # ~12 FPS for smooth animation

        animation_thread = threading.Thread(target=animate_spinner, daemon=True)
        animation_thread.start()

        try:
            yield
        finally:
            stop_event.set()
            animation_thread.join(timeout=0.5)
            if panel in config._matrix_center_content:
                config._matrix_center_content.remove(panel)
            _update_matrix_display()
    else:
        console.print()
        with Live(panel, console=console, refresh_per_second=10):
            yield
        console.print()


@contextmanager
def function_calls_panel():
    """Display function call execution panel.

    Yields:
        List to append function call renderables to
    """
    import assistant.ui.config as config

    renderables = []
    yield renderables

    if renderables:
        panel = Panel(
            Group(*renderables),
            title=f"[bold {COLOR_SECONDARY}]Calling Function[/bold {COLOR_SECONDARY}]",
            title_align="left",
            border_style=COLOR_PRIMARY,
            box=box.ROUNDED,
            padding=(0, 1),
        )

        if config._matrix_live is not None:
            config._matrix_center_content.append(panel)
            _update_matrix_display()
        else:
            console.print()
            console.print(panel)
