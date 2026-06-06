"""Configuration management for Dictionary Bot."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration."""

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    max_tokens: int = 500
    temperature: float = 0.7


def load_config(env_file: Optional[str] = None) -> Config:
    """Load configuration from environment variables.

    Args:
        env_file: Optional path to a .env file. If not provided,
                  python-dotenv searches for a .env file automatically.

    Returns:
        A populated Config instance.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    load_dotenv(dotenv_path=env_file, override=True)

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is required but not set. "
            "Please set it in your environment or .env file."
        )

    return Config(
        openai_api_key=api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "500")),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
    )
