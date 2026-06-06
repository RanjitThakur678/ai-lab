"""Configuration management for Dictionary Bot."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration."""

    provider: str
    api_key: str
    base_url: Optional[str]
    model: str
    max_tokens: int
    temperature: float


def load_config(
    env_file: Optional[str] = None,
    provider: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
) -> Config:
    """Load configuration from environment variables.

    Supports multiple LLM providers:
      - openai    (default)
      - ollama    (local, free)
      - kimchi    (Kimchi built-in provider)
      - custom    (any OpenAI-compatible endpoint)

    Args:
        env_file: Optional path to a .env file.
        provider: Override provider (e.g. "ollama", "kimchi", "openai").
        base_url: Override base URL for the API.
        model: Override model name.

    Returns:
        A populated Config instance.

    Raises:
        ValueError: If required config is missing for the chosen provider.
    """
    load_dotenv(dotenv_path=env_file, override=True)

    chosen_provider = (provider or os.getenv("PROVIDER", "openai")).strip().lower()

    def _env(key: str, default: str = "") -> str:
        return os.getenv(key, default).strip()

    if chosen_provider == "openai":
        api_key = _env("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is required for the 'openai' provider. "
                "Please set it in your environment or .env file."
            )
        resolved_base_url = base_url or _env("OPENAI_BASE_URL") or None
        resolved_model = model or _env("OPENAI_MODEL", "gpt-4o-mini")

    elif chosen_provider == "ollama":
        api_key = _env("OLLAMA_API_KEY", "ollama")
        resolved_base_url = base_url or _env("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        resolved_model = model or _env("OLLAMA_MODEL", "llama3.2")

    elif chosen_provider == "kimchi":
        api_key = _env("KIMCHI_API_KEY") or _env("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "KIMCHI_API_KEY is required for the 'kimchi' provider."
            )
        resolved_base_url = base_url or _env("KIMCHI_BASE_URL", "https://llm.kimchi.dev/openai/v1")
        resolved_model = model or _env("KIMCHI_MODEL", "kimi-k2.5")

    elif chosen_provider == "custom":
        api_key = _env("CUSTOM_API_KEY") or _env("OPENAI_API_KEY")
        resolved_base_url = base_url or _env("CUSTOM_BASE_URL")
        if not resolved_base_url:
            raise ValueError(
                "CUSTOM_BASE_URL is required for the 'custom' provider."
            )
        resolved_model = model or _env("CUSTOM_MODEL", "gpt-4o-mini")
    else:
        raise ValueError(
            f"Unknown provider: '{chosen_provider}'. "
            "Supported: openai, ollama, kimchi, custom."
        )

    if not api_key:
        raise ValueError(
            f"API key is required but not set for provider '{chosen_provider}'."
        )

    return Config(
        provider=chosen_provider,
        api_key=api_key,
        base_url=resolved_base_url or None,
        model=resolved_model,
        max_tokens=int(_env("MAX_TOKENS", "500")),
        temperature=float(_env("TEMPERATURE", "0.7")),
    )
