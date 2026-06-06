"""Tests for dictionary_bot.agent module."""

from unittest.mock import MagicMock, patch

import pytest

from dictionary_bot.agent import DictionaryAgent, DictionaryBotError
from dictionary_bot.config import Config


class TestDictionaryAgent:
    """Tests for DictionaryAgent."""

    @pytest.fixture
    def config(self):
        """Fixture providing a test configuration."""
        return Config(
            openai_api_key="sk-test",
            openai_model="gpt-4o-mini",
            max_tokens=500,
            temperature=0.7,
        )

    @pytest.fixture
    def mock_client(self):
        """Fixture providing a mock OpenAI client."""
        with patch("dictionary_bot.agent.OpenAI") as mock_openai:
            client = MagicMock()
            mock_openai.return_value = client
            yield client

    def test_chat_returns_response(self, config, mock_client):
        """Test that chat returns the assistant's response text."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "A pleasant surprise."
        mock_client.chat.completions.create.return_value = mock_response

        agent = DictionaryAgent(config)
        result = agent.chat("What does 'serendipity' mean?")

        assert result == "A pleasant surprise."
        mock_client.chat.completions.create.assert_called_once()

        # Verify system prompt is included
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert "Lexi" in messages[0]["content"]
        assert messages[1] == {"role": "user", "content": "What does 'serendipity' mean?"}

    def test_chat_maintains_conversation_history(self, config, mock_client):
        """Test that multi-turn conversation is maintained."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "A pleasant surprise."
        mock_client.chat.completions.create.return_value = mock_response

        agent = DictionaryAgent(config)
        agent.chat("What does 'serendipity' mean?")
        agent.chat("Give me a synonym.")

        history = agent.conversation_history
        assert len(history) == 4  # 2 user + 2 assistant
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "What does 'serendipity' mean?"
        assert history[1]["role"] == "assistant"
        assert history[2]["content"] == "Give me a synonym."

        # Verify API was called with full history
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert len(messages) == 4  # system + 3 history items at time of 2nd call

    def test_reset_conversation(self, config, mock_client):
        """Test that reset clears conversation history."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "A pleasant surprise."
        mock_client.chat.completions.create.return_value = mock_response

        agent = DictionaryAgent(config)
        agent.chat("What does 'serendipity' mean?")
        assert len(agent.conversation_history) == 2

        agent.reset_conversation()
        assert len(agent.conversation_history) == 0

    def test_chat_api_error_raises_dictionary_bot_error(self, config, mock_client):
        """Test that API errors are wrapped in DictionaryBotError."""
        from openai import APIError

        mock_client.chat.completions.create.side_effect = APIError(
            message="Server error",
            request=MagicMock(),
            body=None,
        )

        agent = DictionaryAgent(config)
        with pytest.raises(DictionaryBotError, match="OpenAI API error"):
            agent.chat("hello")

    def test_chat_authentication_error(self, config, mock_client):
        """Test that auth errors produce a clear message."""
        from openai import AuthenticationError

        mock_client.chat.completions.create.side_effect = AuthenticationError(
            message="Invalid API key",
            response=MagicMock(),
            body=None,
        )

        agent = DictionaryAgent(config)
        with pytest.raises(DictionaryBotError, match="Invalid OpenAI API key"):
            agent.chat("hello")

    def test_chat_rate_limit_error(self, config, mock_client):
        """Test that rate limit errors produce a clear message."""
        from openai import RateLimitError

        mock_client.chat.completions.create.side_effect = RateLimitError(
            message="Rate limit",
            response=MagicMock(),
            body=None,
        )

        agent = DictionaryAgent(config)
        with pytest.raises(DictionaryBotError, match="Rate limit exceeded"):
            agent.chat("hello")

    def test_history_trimming_on_long_context(self, config, mock_client):
        """Test that old messages are trimmed when history gets long."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "response"
        mock_client.chat.completions.create.return_value = mock_response

        agent = DictionaryAgent(config)

        # Create a very long message to force trimming
        long_msg = "a" * 5000
        for i in range(5):
            agent.chat(f"{i}-{long_msg}")

        # History should have been trimmed to avoid exceeding token limit
        history = agent.conversation_history
        estimated_tokens = sum(len(m["content"]) // 4 for m in history)
        assert estimated_tokens <= DictionaryAgent.MAX_HISTORY_ESTIMATED_TOKENS
