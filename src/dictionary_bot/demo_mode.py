"""Built-in demo mode — no API key or network required."""

from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

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


class DemoAgent:
    """Mock agent for UI demonstration without API calls."""

    def __init__(self) -> None:
        self._last_word: Optional[str] = None

    def chat(self, message: str) -> str:
        lower = message.lower()
        found_word = None
        for word in MOCK_DATA:
            if word in lower:
                found_word = word
                break
        if not found_word and self._last_word:
            found_word = self._last_word

        if not found_word:
            return (
                "I'm not sure which word you're asking about. "
                "Try asking: **What does 'serendipity' mean?**"
            )

        data = MOCK_DATA[found_word]

        if "synonym" in lower or "similar" in lower:
            result = f"**Synonyms for {data['noun']}:**\n\n{data['synonyms']}"
        elif "example" in lower or "sentence" in lower:
            result = f"**Example sentence for {data['noun']}:**\n\n_{data['example']}_"
        elif "antonym" in lower or "opposite" in lower:
            result = (
                f"**Antonyms for {data['noun']}:**\n\n"
                "I don't have antonyms memorized, "
                "but you can think of concepts like permanence, rarity, or scarcity."
            )
        else:
            result = (
                f"**Definition:** {data['noun']} refers to {data['definition']}.\n\n"
                f"**Example:**\n\"{data['example']}\"\n\n"
                f"**Synonyms:** {data['synonyms']}"
            )

        self._last_word = found_word
        return result

    def reset_conversation(self) -> None:
        self._last_word = None

    def run(self) -> None:
        welcome = Text()
        welcome.append("📚 ", style="bold yellow")
        welcome.append("Welcome to Dictionary Bot!\n", style="bold cyan")
        welcome.append("I'm ", style="white")
        welcome.append("Lexi", style="bold magenta")
        welcome.append(", your English dictionary tutor.\n", style="white")
        welcome.append(
            "Ask me about any word — definitions, synonyms, examples, and more!\n",
            style="dim white",
        )
        welcome.append("Type ", style="dim white")
        welcome.append("/help", style="bold green")
        welcome.append(" for commands.", style="dim white")
        console.print(Panel(welcome, border_style="cyan", padding=(1, 2)))

        console.print("[bold red]DEMO MODE[/bold red] — no API calls are being made.\n")

        while True:
            try:
                user_input = Prompt.ask("[bold blue]You[/bold blue]")
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Goodbye! 👋[/dim]")
                return

            user_input = user_input.strip()
            if not user_input:
                continue

            if user_input.lower() in {"/quit", "/exit", "quit", "exit"}:
                console.print("[dim]Goodbye! 👋[/dim]")
                return

            if user_input.lower() == "/reset":
                self.reset_conversation()
                console.print("[dim]Conversation history cleared.[/dim]")
                continue

            with console.status("[bold green]Lexi is thinking...[/bold green]"):
                response = self.chat(user_input)
            md = Markdown(response)
            console.print(Panel(md, border_style="magenta", title="Lexi", title_align="left"))
