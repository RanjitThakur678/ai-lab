"""Interactive CLI for the Dictionary Bot."""

import argparse
import sys
from typing import Optional

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


def _run_demo() -> int:
    """Run the built-in demo mode (no API key required)."""
    from dictionary_bot.demo_mode import DemoAgent

    agent = DemoAgent()
    agent.run()
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """Run the interactive CLI.

    Returns:
        Exit code (0 for clean exit).
    """
    parser = argparse.ArgumentParser(
        description="Dictionary Bot — conversational English tutor",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama", "kimchi", "custom"],
        default=None,
        help="LLM provider to use (default: openai)",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Override the API base URL",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the model name",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo mode without API calls",
    )
    args = parser.parse_args(argv)

    if args.demo:
        return _run_demo()

    try:
        config = load_config(
            provider=args.provider,
            base_url=args.base_url,
            model=args.model,
        )
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        console.print(
            "[dim]Tip: Copy .env.example to .env and configure your provider.[/dim]"
        )
        console.print(
            "[dim]Or run with --demo for a no-API preview.[/dim]"
        )
        return 1

    agent = DictionaryAgent(config)

    print_welcome()
    console.print(f"[dim]Provider: {config.provider} | Model: {config.model}[/dim]")
    console.print()

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
