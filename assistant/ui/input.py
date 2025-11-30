"""User input handling."""

from rich.panel import Panel
from rich.text import Text
from rich import box

from .config import console, COLOR_PRIMARY, COLOR_SECONDARY
from .layout import (
    _get_terminal_height,
    _create_side_panel,
    _create_center_panel,
    _create_layout,
    _update_matrix_display,
)


def get_user_input_in_matrix(prompt_text="You"):
    """Get user input with clean display pause/resume.

    Args:
        prompt_text: Prompt label

    Returns:
        User input string
    """
    import assistant.ui.config as config

    if config._matrix_live is not None:
        config._matrix_live.stop()

        height = _get_terminal_height()
        input_prompt_panel = Panel(
            Text("Type your message below:", style=f"{COLOR_SECONDARY}"),
            title=f"[bold {COLOR_PRIMARY}]{prompt_text}[/bold {COLOR_PRIMARY}]",
            title_align="left",
            border_style=COLOR_PRIMARY,
            box=box.ROUNDED,
            padding=(0, 1),
        )

        temp_content = config._matrix_center_content.copy()
        temp_content.append(input_prompt_panel)

        # Create static layout
        left_panel = _create_side_panel(height)
        center_panel = _create_center_panel(temp_content)
        right_panel = _create_side_panel(height)

        layout = _create_layout(left_panel, center_panel, right_panel)

        # Display the layout with input prompt
        console.clear()
        console.print(layout)
        console.print()

        # Get input with styled prompt
        try:
            user_input = console.input(
                f"[bold {COLOR_PRIMARY}]> [/bold {COLOR_PRIMARY}]"
            )
        except (EOFError, KeyboardInterrupt):
            user_input = ""

        # Add message to content
        if user_input.strip():
            message_panel = Panel(
                Text(user_input, style="white"),
                title="[bold cyan]User Message[/bold cyan]",
                title_align="left",
                border_style=COLOR_PRIMARY,
                box=box.ROUNDED,
                padding=(0, 1),
            )
            config._matrix_center_content.append(message_panel)

        config._matrix_live.start()
        _update_matrix_display()
    else:
        user_input = console.input(
            f"[bold {COLOR_PRIMARY}]You >[/bold {COLOR_PRIMARY}] "
        )

    return user_input
