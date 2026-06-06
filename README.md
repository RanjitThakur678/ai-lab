# 📚 Dictionary Bot

A conversational English dictionary chatbot powered by LLMs. Ask for definitions, synonyms, antonyms, example sentences, pronunciation help, etymology, and grammar tips — all through a beautiful interactive CLI.

**Multi-provider support:** OpenAI, Ollama (local), Kimchi, or any OpenAI-compatible endpoint.

## Features

- **Multi-provider** — Switch between OpenAI, local Ollama, Kimchi, or custom endpoints
- **Conversational** — Multi-turn chat with context memory
- **Beautiful CLI** — Styled with `rich` for an elegant terminal experience
- **Smart History** — Automatically trims old messages to stay within token limits
- **Graceful Errors** — Clear, friendly error messages for API issues
- **Demo Mode** — Run without any API key for UI testing
- **Easy Setup** — One `.env` file and you're ready to go

## Quick Start

### 1. Clone & Install

```bash
cd ai-lab
pip install -e ".[dev]"
```

### 2. Choose your provider

#### Option A: OpenAI (default)
```bash
cp .env.example .env
# Add your OPENAI_API_KEY
```

#### Option B: Ollama (local, free)
```bash
# Install Ollama: https://ollama.com
ollama pull llama3.2

# No API key needed — just set provider
echo 'PROVIDER=ollama' >> .env
```

#### Option C: Demo mode (no API at all)
```bash
python3 -m dictionary_bot --demo
# or: dictionary-bot --demo
```

### 3. Run

```bash
# Default: uses OpenAI
python3 -m dictionary_bot

# Or use the installed command
python3 -m dictionary_bot --provider ollama --model llama3.2
```

## CLI Options

```bash
python3 -m dictionary_bot --help
```

| Flag | Description |
|------|-------------|
| `--demo` | Run demo mode without API calls |
| `--provider {openai,ollama,kimchi,custom}` | Choose LLM provider |
| `--base-url URL` | Override API base URL |
| `--model MODEL` | Override model name |

## Example Session

```
📚 Welcome to Dictionary Bot!
I'm Lexi, your English dictionary tutor.
Ask me about any word — definitions, synonyms, examples, and more!
Type /help for commands.

Provider: openai | Model: gpt-4o-mini

❯ What does "serendipity" mean?

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

## Chat Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help message |
| `/reset` | Clear conversation history |
| `/quit` | Exit the chat |
| `/exit` | Exit the chat (alias) |

## Provider Configuration

| Provider | Required ENV | Optional ENV |
|----------|-------------|-------------|
| **openai** | `OPENAI_API_KEY` | `OPENAI_BASE_URL`, `OPENAI_MODEL` |
| **ollama** | — | `OLLAMA_BASE_URL` (default: localhost:11434) |
| **kimchi** | `KIMCHI_API_KEY` | `KIMCHI_BASE_URL`, `KIMCHI_MODEL` |
| **custom** | `CUSTOM_API_KEY` | `CUSTOM_BASE_URL`, `CUSTOM_MODEL` |

Shared config: `MAX_TOKENS`, `TEMPERATURE`

See `.env.example` for the full template.

## Docker

```bash
# Build & run with your API key
docker build -t dictionary-bot:latest .
docker run -it --env-file .env dictionary-bot:latest

# Or use docker-compose
docker compose up
```

## Running Tests

```bash
# Unit tests (fast, free, no API calls)
python3 -m pytest tests/ -m "not e2e" -v

# E2E tests with real API (requires API key)
python3 -m pytest tests/test_e2e.py -m e2e -v

# Coverage
python3 -m pytest tests/ -m "not e2e" --cov=src/dictionary_bot --cov-report=html
```

## Project Structure

```
ai-lab/
├── src/dictionary_bot/
│   ├── __init__.py
│   ├── __main__.py       # python -m dictionary_bot
│   ├── agent.py          # Core AI agent (multi-provider)
│   ├── cli.py            # Rich CLI with argparse
│   ├── config.py         # Multi-provider config loader
│   ├── demo_mode.py      # Offline demo agent
│   └── prompts.py        # System prompt
├── tests/
│   ├── test_agent.py
│   ├── test_config.py
│   ├── test_e2e.py
│   └── test_prompts.py
├── demo.py               # Standalone demo script
├── test_batch.py         # Batch evaluation script
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
