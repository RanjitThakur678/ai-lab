"""Tests for dictionary_bot.config module."""

import os
from unittest.mock import patch

import pytest

from dictionary_bot.config import Config, load_config


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_openai_defaults(self, tmp_path, monkeypatch):
        """Test loading config with OpenAI provider defaults."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "OPENAI_API_KEY=sk-test-key\n"
        )

        config = load_config(str(env_file))

        assert isinstance(config, Config)
        assert config.provider == "openai"
        assert config.api_key == "sk-test-key"
        assert config.model == "gpt-4o-mini"
        assert config.base_url is None
        assert config.max_tokens == 500
        assert config.temperature == 0.7

    def test_load_config_with_optional_overrides(self, tmp_path, monkeypatch):
        """Test that optional env vars override defaults."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "OPENAI_API_KEY=sk-test-key\n"
            "OPENAI_BASE_URL=https://custom.openai.com/v1\n"
            "OPENAI_MODEL=gpt-4o\n"
            "MAX_TOKENS=1000\n"
            "TEMPERATURE=0.5\n"
        )

        config = load_config(str(env_file))

        assert config.provider == "openai"
        assert config.base_url == "https://custom.openai.com/v1"
        assert config.model == "gpt-4o"
        assert config.max_tokens == 1000
        assert config.temperature == 0.5

    def test_load_config_openai_missing_key(self, tmp_path, monkeypatch):
        """Test that missing OPENAI_API_KEY raises ValueError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text("SOME_OTHER_VAR=value\n")

        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            load_config(str(env_file))

    def test_load_config_openai_empty_key(self, tmp_path, monkeypatch):
        """Test that empty OPENAI_API_KEY raises ValueError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text("OPENAI_API_KEY=   \n")

        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            load_config(str(env_file))

    def test_load_config_ollama(self, tmp_path, monkeypatch):
        """Test loading config with Ollama provider."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "PROVIDER=ollama\n"
            "OLLAMA_MODEL=llama3.2\n"
        )

        config = load_config(str(env_file))

        assert config.provider == "ollama"
        assert config.api_key == "ollama"
        assert config.base_url == "http://localhost:11434/v1"
        assert config.model == "llama3.2"

    def test_load_config_kimchi(self, tmp_path, monkeypatch):
        """Test loading config with Kimchi provider."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "PROVIDER=kimchi\n"
            "KIMCHI_API_KEY=kimchi-test-key\n"
        )

        config = load_config(str(env_file))

        assert config.provider == "kimchi"
        assert config.api_key == "kimchi-test-key"
        assert config.base_url == "https://llm.kimchi.dev/openai/v1"
        assert config.model == "kimi-k2.5"

    def test_load_config_custom(self, tmp_path, monkeypatch):
        """Test loading config with custom provider."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "PROVIDER=custom\n"
            "CUSTOM_API_KEY=custom-key\n"
            "CUSTOM_BASE_URL=https://api.example.com/v1\n"
            "CUSTOM_MODEL=custom-model\n"
        )

        config = load_config(str(env_file))

        assert config.provider == "custom"
        assert config.api_key == "custom-key"
        assert config.base_url == "https://api.example.com/v1"
        assert config.model == "custom-model"

    def test_load_config_custom_missing_base_url(self, tmp_path, monkeypatch):
        """Test that custom provider without base URL raises ValueError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("CUSTOM_BASE_URL", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "PROVIDER=custom\n"
            "CUSTOM_API_KEY=custom-key\n"
        )

        with pytest.raises(ValueError, match="CUSTOM_BASE_URL is required"):
            load_config(str(env_file))

    def test_load_config_unknown_provider(self, tmp_path, monkeypatch):
        """Test that unknown provider raises ValueError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "PROVIDER=unknown\n"
        )

        with pytest.raises(ValueError, match="Unknown provider"):
            load_config(str(env_file))

    def test_load_config_with_args_override(self, tmp_path, monkeypatch):
        """Test that function args override env vars."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text(
            "OPENAI_API_KEY=sk-test-key\n"
            "OPENAI_MODEL=gpt-4o-mini\n"
        )

        config = load_config(
            str(env_file),
            provider="ollama",
            model="llama3.2",
        )

        assert config.provider == "ollama"
        assert config.model == "llama3.2"
        # api_key comes from ollama default since we switched provider
        assert config.api_key == "ollama"
