"""Configuration constants and global state for the UI package."""

from rich.console import Console

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

MATRIX_PANEL_WIDTH = 22
MAX_VISIBLE_MESSAGES = 10

COLOR_PRIMARY = "magenta"
COLOR_SECONDARY = "cyan"
COLOR_SUCCESS = "green"
COLOR_ERROR = "red"
COLOR_WARNING = "yellow"
COLOR_MATRIX = "green"

# =============================================================================
# GLOBAL STATE
# =============================================================================

console = Console()

_matrix_live = None
_matrix_center_content = []
