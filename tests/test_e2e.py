"""End-to-end functional tests for Dictionary Bot.

These tests hit the real OpenAI API and are skipped by default.
Run them explicitly with:
    python3 -m pytest tests/test_e2e.py -v -m e2e

Or run the script directly:
    python3 tests/test_e2e.py

Note: These tests cost API tokens. Only run when you want to verify
real-world behavior.
"""

import os

import pytest

from dictionary_bot.config import Config, load_config
from dictionary_bot.agent import DictionaryAgent

pytestmark = pytest.mark.e2e


def _get_config():
    """Helper to skip if API key is not available."""
    try:
        return load_config()
    except ValueError:
        pytest.skip("OPENAI_API_KEY not configured — skipping E2E test")


def test_word_definition():
    """Agent returns a coherent definition for a known word."""
    config = _get_config()
    agent = DictionaryAgent(config)

    response = agent.chat('What does "serendipity" mean?')

    assert isinstance(response, str) and len(response) > 20
    assert "serendipity" not in response.lower() or "pleasant" in response.lower()
    # Should contain definitional content, not just echo the word
    assert any(
        clue in response.lower()
        for clue in ["pleasant", "surprise", "chance", "finding", "unexpected", "discover"]
    )


def test_conversation_memory():
    """Agent remembers the previous word in a follow-up question."""
    config = _get_config()
    agent = DictionaryAgent(config)

    agent.chat('What does "serendipity" mean?')
    response = agent.chat("Give me a synonym")

    assert isinstance(response, str) and len(response) > 10
    # Should mention synonyms or related words, not ask "what word?"
    assert "what word" not in response.lower()
    assert "which word" not in response.lower()


def test_example_sentence():
    """Agent can provide a usage example."""
    config = _get_config()
    agent = DictionaryAgent(config)

    agent.chat('What does "ephemeral" mean?')
    response = agent.chat("Use it in a sentence")

    assert "ephemeral" in response.lower()
    assert any(punct in response for punct in [".", "!", "?"])


def test_reset_clears_context():
    """Resetting conversation removes prior context."""
    config = _get_config()
    agent = DictionaryAgent(config)

    agent.chat('What does "serendipity" mean?')
    agent.reset_conversation()

    # Ask a vague follow-up — without context it should not know the word
    response = agent.chat("Give me a synonym")
    # A reset agent should not be able to infer which word is meant
    assert "serendipity" not in response.lower()


def test_multiple_definitions():
    """Agent handles a word with multiple meanings."""
    config = _get_config()
    agent = DictionaryAgent(config)

    response = agent.chat('What does "run" mean?')

    assert isinstance(response, str) and len(response) > 30
    # Should mention at least one meaning (verb or noun)
    assert any(word in response.lower() for word in ["move", "fast", "operate", "jog", "race"])


if __name__ == "__main__":
    """Run E2E tests directly without pytest."""
    try:
        cfg = load_config()
    except ValueError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    tests = [
        test_word_definition,
        test_conversation_memory,
        test_example_sentence,
        test_reset_clears_context,
        test_multiple_definitions,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as exc:
            print(f"❌ {test.__name__}: {exc}")
            failed += 1
        except Exception as exc:
            print(f"💥 {test.__name__}: {exc}")
            failed += 1

    print(f"\n{'🎉' if failed == 0 else '⚠️'} {passed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)
