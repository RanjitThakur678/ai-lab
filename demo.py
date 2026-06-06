"""Mock demo of Dictionary Bot — no API key needed.

Simulates Lexi for demonstration and UI testing purposes.
Usage:
    python3 demo.py
"""

import sys
from typing import Optional, Tuple

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

MOCK_RESPONSES = {
    "default": """
**Definition:**
{noun} refers to {definition}.

**Example:**
"{example}"

**Synonyms:** {synonyms}
    """,
}

MOCK_DATA = {
    "serendipity": {
        "noun": "Serendipity",
        "definition": "finding something good without looking for it — a pleasant surprise",
        "example": "It was pure serendipity that I found my dream job while browsing a bookstore.",
        "synonyms": "chance, fluke, happy accident, fortuity",
    },
    "ephemeral": {
        "noun": "Ephemeral",
        "definition": "lasting for a very short time; transient or fleeting",
        "example": "The beauty of cherry blossoms is ephemeral, lasting only a few weeks each spring.",
        "synonyms": "transient, fleeting, momentary, short-lived",
    },
    "ubiquitous": {
        "noun": "Ubiquitous",
        "definition": "present, appearing, or found everywhere",
        "example": "Smartphones have become ubiquitous in modern society.",
        "synonyms": "omnipresent, pervasive, universal, widespread",
    },
}


def print_welcome() -> None:
    welcome_text = Text()
    welcome_text.append("📚 ", style="bold yellow")
    welcome_text.append("Welcome to Dictionary Bot!\n", style="bold cyan")
    welcome_text.append("I'm ", style="white")
    welcome_text.append("Lexi", style="bold magenta")
    welcome_text.append(", your English dictionary tutor.\n", style="white")
    welcome_text.append(
        "Ask me about any word — definitions, synonyms, examples, and more!\n",
        style="dim white",
    )
    welcome_text.append("Type ", style="dim white")
    welcome_text.append("/help", style="bold green")
    welcome_text.append(" for commands.", style="dim white")
    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2)))


def print_help() -> None:
    help_md = """
**Available Commands:**

- `/help` — Show this help message
- `/reset` — Reset the conversation history
- `/quit` or `/exit` — Exit the chat

Just type any word or question to chat with Lexi!
    """
    console.print(Panel(Markdown(help_md), border_style="green", title="Help"))


def print_response(text: str) -> None:
    md = Markdown(text)
    console.print(Panel(md, border_style="magenta", title="Lexi", title_align="left"))


def get_mock_response(user_input: str, last_word: Optional[str]) -> Tuple[str, Optional[str]]:
    lower = user_input.lower()

    # Extract a word from the query
    found_word = None
    for word in MOCK_DATA:
        if word in lower:
            found_word = word
            break

    if not found_word and last_word:
        found_word = last_word

    if not found_word:
        return (
            "I'm not sure which word you're asking about. "
            "Try asking: **What does 'serendipity' mean?**",
            None,
        )

    data = MOCK_DATA[found_word]

    if "synonym" in lower or "similar" in lower:
        return (
            f"**Synonyms for {data['noun']}:**\n\n{data['synonyms']}",
            found_word,
        )
    elif "example" in lower or "sentence" in lower:
        return (
            f"**Example sentence for {data['noun']}:**\n\n_{data['example']}_",
            found_word,
        )
    elif "antonym" in lower or "opposite" in lower:
        return (
            f"**Antonyms for {data['noun']}:**\n\nI don't have antonyms memorized, "
            "but you can think of concepts like permanence, rarity, or scarcity.",
            found_word,
        )
    else:
        return (
            MOCK_RESPONSES["default"].format(**data),
            found_word,
        )


def main() -> int:
    print_welcome()
    last_word = None

    while True:
        try:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
        except (EOFError, KeyboardInterrupt):
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
            last_word = None
            console.print("[dim]Conversation history cleared.[/dim]")
            continue

        with console.status("[bold green]Lexi is thinking...[/bold green]"):
            response, last_word = get_mock_response(user_input, last_word)
        print_response(response)

    return 0


if __name__ == "__main__":
    sys.exit(main())
