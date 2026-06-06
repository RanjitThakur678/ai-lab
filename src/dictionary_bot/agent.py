"""Core AI agent logic for the Dictionary Bot."""

from openai import OpenAI, APIError, AuthenticationError, RateLimitError

from dictionary_bot.config import Config
from dictionary_bot.prompts import SYSTEM_PROMPT


class DictionaryBotError(Exception):
    """Custom exception for Dictionary Bot errors."""

    pass


class DictionaryAgent:
    """A conversational English dictionary agent powered by OpenAI."""

    MAX_HISTORY_ESTIMATED_TOKENS = 8000
    AVG_CHARS_PER_TOKEN = 4

    def __init__(self, config: Config) -> None:
        """Initialize the agent with the given configuration.

        Args:
            config: Application configuration including API key and model.
        """
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)
        self._history: list[dict[str, str]] = []

    def chat(self, message: str) -> str:
        """Send a message to the agent and return the response.

        Args:
            message: The user's message.

        Returns:
            The assistant's response text.

        Raises:
            DictionaryBotError: If the API call fails.
        """
        self._history.append({"role": "user", "content": message})
        self._trim_history()

        messages = self._build_messages()

        try:
            response = self._client.chat.completions.create(
                model=self._config.openai_model,
                messages=messages,
                max_tokens=self._config.max_tokens,
                temperature=self._config.temperature,
            )
        except AuthenticationError as exc:
            raise DictionaryBotError(
                "Invalid OpenAI API key. Please check your OPENAI_API_KEY."
            ) from exc
        except RateLimitError as exc:
            raise DictionaryBotError(
                "Rate limit exceeded. Please wait a moment and try again."
            ) from exc
        except APIError as exc:
            raise DictionaryBotError(
                f"OpenAI API error: {exc.message}"
            ) from exc
        except Exception as exc:
            raise DictionaryBotError(
                f"Unexpected error: {exc}"
            ) from exc

        content = response.choices[0].message.content or ""
        self._history.append({"role": "assistant", "content": content})
        return content

    def reset_conversation(self) -> None:
        """Clear the conversation history, keeping only the system prompt."""
        self._history.clear()

    @property
    def conversation_history(self) -> list[dict[str, str]]:
        """Return a copy of the current conversation history."""
        return list(self._history)

    def _build_messages(self) -> list[dict[str, str]]:
        """Build the full message list including system prompt."""
        return [{"role": "system", "content": SYSTEM_PROMPT}, *self._history]

    def _trim_history(self) -> None:
        """Trim oldest non-system messages if history is too long."""
        estimated_tokens = sum(
            len(msg["content"]) // self.AVG_CHARS_PER_TOKEN
            for msg in self._history
        )

        while (
            estimated_tokens > self.MAX_HISTORY_ESTIMATED_TOKENS
            and len(self._history) > 1
        ):
            removed = self._history.pop(0)
            estimated_tokens -= len(removed["content"]) // self.AVG_CHARS_PER_TOKEN
