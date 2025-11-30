"""Border and layout generation utilities."""

from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.console import Group
from rich import box

from .config import (
    MATRIX_PANEL_WIDTH,
    MAX_VISIBLE_MESSAGES,
    COLOR_PRIMARY,
    COLOR_MATRIX,
    console,
)


def _create_cyberpunk_border(height):
    """Create static ASCII cyberpunk border pattern.

    Args:
        height: Number of lines to generate

    Returns:
        Rich Text object with ASCII patterns
    """
    text = Text()
    width = MATRIX_PANEL_WIDTH - 2

    ascii_patterns = ["=", "-", "#", "=#-"]

    for i in range(height):
        pattern = ascii_patterns[i % 4]
        if pattern == "=#-":
            line = (pattern * (width // 3 + 1))[:width]
        else:
            line = pattern * width

        # Gradient effect: bold → normal → dim
        if i < height // 3:
            style = f"bold {COLOR_MATRIX}"
        elif i < 2 * height // 3:
            style = COLOR_MATRIX
        else:
            style = f"dim {COLOR_MATRIX}"

        text.append(line + "\n", style=style)

    return text


def _get_terminal_height():
    """Get current terminal height with fallback."""
    try:
        return max(console.size.height - 4, 20)
    except Exception:
        return 30


def _create_side_panel(height):
    """Create a side panel with cyberpunk border.

    Args:
        height: Panel height in lines

    Returns:
        Rich Panel with ASCII border pattern
    """
    return Panel(
        _create_cyberpunk_border(height),
        border_style=f"dim {COLOR_MATRIX}",
        box=box.ROUNDED,
        padding=(0, 0),
    )


def _create_center_panel(content_list):
    """Create center panel with message history.

    Args:
        content_list: List of Rich renderable objects

    Returns:
        Rich Panel with formatted content
    """
    display_content = (
        content_list[-MAX_VISIBLE_MESSAGES:]
        if len(content_list) > MAX_VISIBLE_MESSAGES
        else content_list
    )

    if display_content:
        spaced_content = []
        for i, item in enumerate(display_content):
            spaced_content.append(item)
            if i < len(display_content) - 1:
                spaced_content.append(Text(""))
        content = Group(*spaced_content)
    else:
        content = Text("")

    return Panel(
        content,
        border_style=f"bold {COLOR_PRIMARY}",
        box=box.HEAVY,
        padding=(0, 1),
    )


def _create_layout(left_panel, center_panel, right_panel):
    """Create three-column layout with fixed border widths.

    Args:
        left_panel: Left border panel
        center_panel: Center content panel
        right_panel: Right border panel

    Returns:
        Rich Layout object
    """
    layout = Layout()
    layout.split_row(
        Layout(left_panel, size=MATRIX_PANEL_WIDTH),
        Layout(center_panel, ratio=1),
        Layout(right_panel, size=MATRIX_PANEL_WIDTH),
    )
    return layout


def _update_matrix_display():
    """Update Live display with current content."""
    from .config import _matrix_live, _matrix_center_content

    if _matrix_live is None:
        return

    height = _get_terminal_height()
    left_panel = _create_side_panel(height)
    center_panel = _create_center_panel(_matrix_center_content)
    right_panel = _create_side_panel(height)

    layout = _create_layout(left_panel, center_panel, right_panel)
    _matrix_live.update(layout)
