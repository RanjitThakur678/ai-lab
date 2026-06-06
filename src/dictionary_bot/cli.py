"""Interactive CLI for the Dictionary Bot."""

import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from dictionary_bot.agent import DictionaryAgent, DictionaryBotError
from dictionary_bot.config import Config, load_config


console = Console()


def print_welcome() -> None:
    """Print the welcome banner."""
    welcome_text = Text()
    welcome_text.append("📚 ", style="bold yellow")
    welcome_text.append("Welcome to Dictionary Bot!\n", style="bold cyan")
    welcome_text.append("I'm ", style="white")
    welcome_text.append("Lexi", style="bold magenta")
    welcome_text.append(", your English dictionary tutor.\n", style="white"
    )
    welcome_text.append(
        "Ask me about any word — definitions, synonyms, examples, and more!\n",
        style="dim white",
    )
    welcome_text.append("Type ", style="dim white")
    welcome_text.append("/help", style="bold green")
    welcome_text.append(" for commands.", style="dim white")
    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2)))


def print_help() -> None:
    """Print the help panel."""
    help_md = """
**Available Commands:**

- `/help` — Show this help message
- `/reset` — Reset the conversation history
- `/quit` or `/exit` — Exit the chat

Just type any word or question to chat with Lexi!
    """
    console.print(Panel(Markdown(help_md), border_style="green", title="Help"))


def print_response(text: str) -> None:
    """Render the assistant's response in a styled panel."""
    md = Markdown(text)
    console.print(Panel(md, border_style="magenta", title="Lexi", title_align="left"))


def print_error(message: str) -> None:
    """Render an error message."""
    console.print(Panel(message, border_style="red", title="Error"))


def main() -> int:
    """Run the interactive CLI.

    Returns:
        Exit code (0 for clean exit).
    """
    try:
        config = load_config()
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        console.print(
            "[dim]Tip: Copy .env.example to .env and add your OPENAI_API_KEY.[/dim]"
        )
        return 1

    agent = DictionaryAgent(config)

    print_welcome()

    while True:
        try:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
        except EOFError:
            break
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye! 👋[/dim]")
            return 0

        user_input = user_input.strip()
        if not user_input:
            continue

        if user_input.lower() in {"/quit", "/exit", "quit", "exit"}:
            console.print("[dim]Goodbye! 👋[/dim]")
            return 0

        if user_input.lower() == "/help":
            print_help()
            continue

        if user_input.lower() == "/reset":
            agent.reset_conversation()
            console.print("[dim]Conversation history cleared.[/dim]")
            continue

        try:
            with console.status("[bold green]Lexi is thinking...[/bold green]"):
                response = agent.chat(user_input)
        except DictionaryBotError as exc:
            print_error(str(exc))
            continue
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye! 👋[/dim]")
            return 0

        print_response(response)

    return 0


if __name__ == "__main__":
    sys.exit(main())
