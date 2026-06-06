# 📚 Dictionary Bot

A conversational English dictionary chatbot powered by OpenAI. Ask for definitions, synonyms, antonyms, example sentences, pronunciation help, etymology, and grammar tips — all through a beautiful interactive CLI.

## Features

- **Conversational** — Multi-turn chat with context memory
- **Beautiful CLI** — Styled with `rich` for an elegant terminal experience
- **Smart History** — Automatically trims old messages to stay within token limits
- **Graceful Errors** — Clear, friendly error messages for API issues
- **Easy Setup** — One `.env` file and you're ready to go

## Quick Start

### 1. Clone & Install

```bash
cd ai-lab
pip install -e ".[dev]"
```

### 2. Configure

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-your-key-here
```

> Get your API key at: https://platform.openai.com/api-keys

### 3. Run

```bash
python -m dictionary_bot
```

Or use the installed command:

```bash
dictionary-bot
```

## Example Session

```
📚 Welcome to Dictionary Bot!
I'm Lexi, your English dictionary tutor.
Ask me about any word — definitions, synonyms, examples, and more!
Type /help for commands.

╭──────────────────────────────────────────────────────────────╮
│ ❯ What does "serendipity" mean?                              │
╰──────────────────────────────────────────────────────────────╯

Lexi
  ╭────────────────────────────────────────────────────────────╮
│ **Serendipity** means finding something good without        │
│ looking for it — a pleasant surprise.                       │
│                                                             │
│ **Example:**                                                │
│ "It was pure serendipity that I found my dream job while    │
│ browsing a bookstore."                                      │
│                                                             │
│ **Synonyms:** chance, fluke, happy accident                 │
╰─────────────────────────────────────────────────────────────╯

❯ Give me a synonym
...
```

## CLI Commands

| Command      | Description                      |
|--------------|----------------------------------|
| `/help`      | Show help message                |
| `/reset`     | Clear conversation history       |
| `/quit`      | Exit the chat                    |
| `/exit`      | Exit the chat (alias)            |

## Environment Variables

| Variable              | Default       | Description                         |
|-----------------------|---------------|-------------------------------------|
| `OPENAI_API_KEY`      | *required*    | Your OpenAI API key                 |
| `OPENAI_MODEL`        | `gpt-4o-mini` | Model to use for completions        |
| `OPENAI_MAX_TOKENS`   | `500`         | Maximum tokens per response         |
| `OPENAI_TEMPERATURE`  | `0.7`         | Sampling temperature (0.0 – 2.0)    |

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=dictionary_bot --cov-report=html
```

## Project Structure

```
ai-lab/
├── src/dictionary_bot/
│   ├── __init__.py       # Package init
│   ├── __main__.py       # python -m dictionary_bot
│   ├── agent.py          # Core AI agent & OpenAI integration
│   ├── cli.py            # Rich CLI interface
│   ├── config.py         # Configuration & env loading
│   └── prompts.py        # System prompt templates
├── tests/                # Pytest test suite
├── pyproject.toml        # Package config
├── requirements.txt      # Dependencies
└── .env.example          # Example environment file
```

## License

MIT
