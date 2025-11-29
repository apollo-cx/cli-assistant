"""UI utilities for rich formatting and plain text output"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

console = Console()


def print_function_call(function_name, args, plain=False):
    """Show function call with spinner or plain text"""
    if plain:
        print(f"→ {function_name}({args})")
    else:
        # Return spinner text for use with console.status()
        return f"[cyan]{function_name}[/cyan] [yellow]({args})[/yellow]"


def print_function_complete(function_name, plain=False):
    """Show function completion"""
    if plain:
        print(f"✓ {function_name} completed")
    else:
        console.print(
            f"[bold green]✓[/bold green] [cyan]{function_name}[/cyan] completed"
        )


def print_response(text, plain=False):
    """Print AI response with formatting"""
    if plain:
        print("\n" + "=" * 50)
        print("AI Response:")
        print("=" * 50)
        print(text)
    else:
        console.print(
            Panel(
                Markdown(text),
                title="[bold green]✨ AI Response[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )


def print_verbose_response(response_data, plain=False):
    """Print verbose function response"""
    if plain:
        print(f"→ Response: {response_data}")
    else:
        console.print(
            Panel(
                str(response_data), title=f"[cyan]Response[/cyan]", border_style="cyan"
            )
        )


def print_error(message, plain=False):
    """Print error message"""
    if plain:
        print(f"✗ {message}")
    else:
        console.print(f"[bold red]✗[/bold red] {message}")


def print_success(message, plain=False):
    """Print success message"""
    if plain:
        print(f"✓ {message}")
    else:
        console.print(f"[bold green]✓[/bold green] {message}")


def print_warning(message, plain=False):
    """Print warning message"""
    if plain:
        print(f"! {message}")
    else:
        console.print(f"[yellow]![/yellow] {message}")


def print_request_info(user_prompt, response=None, plain=False):
    """Print request information including prompt and token usage"""
    if plain:
        print("\n" + "=" * 50)
        print("Request Information:")
        print("=" * 50)
        print(f"Prompt: {user_prompt}")
        if response:
            # Try to extract token usage if available
            try:
                if hasattr(response, "usage_metadata"):
                    metadata = response.usage_metadata
                    print(f"Prompt tokens: {metadata.prompt_token_count}")
                    print(f"Response tokens: {metadata.candidates_token_count}")
                    print(f"Total tokens: {metadata.total_token_count}")
            except:
                pass
        print("=" * 50 + "\n")
    else:
        table = Table(title="📊 Request Information", border_style="blue")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row(
            "User Prompt",
            user_prompt[:100] + "..." if len(user_prompt) > 100 else user_prompt,
        )

        if response:
            try:
                if hasattr(response, "usage_metadata"):
                    metadata = response.usage_metadata
                    table.add_row("Prompt Tokens", str(metadata.prompt_token_count))
                    table.add_row(
                        "Response Tokens", str(metadata.candidates_token_count)
                    )
                    table.add_row("Total Tokens", str(metadata.total_token_count))
            except:
                pass

        console.print(table)
