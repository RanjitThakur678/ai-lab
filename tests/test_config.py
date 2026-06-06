"""Tests for dictionary_bot.config module."""

import os
from unittest.mock import patch

import pytest

from dictionary_bot.config import Config, load_config


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_with_valid_env(self, tmp_path):
        """Test loading config with all required env vars set."""
        env_file = tmp_path / ".env"
        env_file.write_text("OPENAI_API_KEY=sk-test-key\n")

        config = load_config(str(env_file))

        assert isinstance(config, Config)
        assert config.openai_api_key == "sk-test-key"
        assert config.openai_model == "gpt-4o-mini"
        assert config.max_tokens == 500
        assert config.temperature == 0.7

    def test_load_config_with_optional_overrides(self, tmp_path):
        """Test that optional env vars override defaults."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "OPENAI_API_KEY=sk-test-key\n"
            "OPENAI_MODEL=gpt-4o\n"
            "OPENAI_MAX_TOKENS=1000\n"
            "OPENAI_TEMPERATURE=0.5\n"
        )

        config = load_config(str(env_file))

        assert config.openai_model == "gpt-4o"
        assert config.max_tokens == 1000
        assert config.temperature == 0.5

    def test_load_config_missing_api_key(self, tmp_path, monkeypatch):
        """Test that missing OPENAI_API_KEY raises ValueError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text("SOME_OTHER_VAR=value\n")

        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            load_config(str(env_file))

    def test_load_config_empty_api_key(self, tmp_path, monkeypatch):
        """Test that empty OPENAI_API_KEY raises ValueError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text("OPENAI_API_KEY=   \n")

        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            load_config(str(env_file))
