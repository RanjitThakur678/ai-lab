"""Tests for dictionary_bot.prompts module."""

from dictionary_bot.prompts import SYSTEM_PROMPT


class TestSystemPrompt:
    """Tests for the system prompt."""

    def test_system_prompt_is_non_empty(self):
        """System prompt must not be empty."""
        assert SYSTEM_PROMPT
        assert len(SYSTEM_PROMPT) > 100

    def test_system_prompt_contains_key_instructions(self):
        """System prompt must cover core dictionary capabilities."""
        prompt_lower = SYSTEM_PROMPT.lower()
        assert "definition" in prompt_lower
        assert "synonym" in prompt_lower
        assert "antonym" in prompt_lower
        assert "example" in prompt_lower
        assert "pronunciation" in prompt_lower
        assert "etymology" in prompt_lower
        assert "grammar" in prompt_lower

    def test_system_prompt_mentions_markdown(self):
        """System prompt should instruct the model to use markdown."""
        assert "markdown" in SYSTEM_PROMPT.lower()
