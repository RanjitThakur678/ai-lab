"""Batch evaluation script for Dictionary Bot.

Runs the bot against a curated list of words and prints a summary.
Usage:
    python3 test_batch.py
    python3 test_batch.py --words ephemeral ubiquitous serendipity
    python3 test_batch.py --output results.json
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime

from dictionary_bot.config import load_config
from dictionary_bot.agent import DictionaryAgent


@dataclass
class EvaluationResult:
    word: str
    query: str
    response: str = ""
    passed: bool = False
    error: str = ""
    duration_ms: float = 0.0
    tokens_estimate: int = 0


DEFAULT_WORDS = [
    "serendipity",
    "ephemeral",
    "ubiquitous",
    "mellifluous",
    "perspicacious",
    "loquacious",
    "ineffable",
    "sonder",
    "petrichor",
    "defenestration",
]


def evaluate_word(agent: DictionaryAgent, word: str) -> EvaluationResult:
    import time

    result = EvaluationResult(word=word, query=f"What does '{word}' mean?")
    start = time.perf_counter()

    try:
        response = agent.chat(result.query)
        result.response = response
        result.duration_ms = (time.perf_counter() - start) * 1000
        result.tokens_estimate = len(response) // 4

        # Basic heuristics for a valid dictionary response
        lower = response.lower()
        checks = [
            len(response) > 50,  # Not too short
            word not in lower[:50] or len(response) > 100,  # Not just echoing
            any(c.isalpha() for c in response),  # Contains text
        ]
        result.passed = all(checks)

    except Exception as exc:
        result.error = f"{type(exc).__name__}: {exc}"
        result.passed = False

    return result


def print_summary(results: list[EvaluationResult]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.passed and not r.error)
    errors = sum(1 for r in results if r.error)
    avg_time = sum(r.duration_ms for r in results if not r.error) / max(total - errors, 1)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total:    {total}")
    print(f"Passed:   {passed}")
    print(f"Failed:   {total - passed - errors}")
    print(f"Errors:   {errors}")
    print(f"Avg time: {avg_time:.0f} ms")
    print("=" * 60)

    for r in results:
        status = "✅" if r.passed and not r.error else ("💥" if r.error else "❌")
        detail = f"({r.error})" if r.error else f"({r.duration_ms:.0f} ms, ~{r.tokens_estimate} tokens)"
        print(f"{status} {r.word:<20} {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch evaluation for Dictionary Bot")
    parser.add_argument(
        "--words", nargs="+", default=None, help="Words to evaluate (default: built-in list)"
    )
    parser.add_argument(
        "--output", default=None, help="Save results to JSON file"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=None, help="Override max_tokens for this run"
    )
    args = parser.parse_args()

    try:
        config = load_config()
    except ValueError as exc:
        print(f"❌ Configuration error: {exc}")
        return 1

    if args.max_tokens:
        config.max_tokens = args.max_tokens

    agent = DictionaryAgent(config)
    words = args.words or DEFAULT_WORDS

    print(f"Evaluating {len(words)} word(s) with model={config.openai_model}...\n")

    results: list[EvaluationResult] = []
    for word in words:
        agent.reset_conversation()  # Fresh context per word
        result = evaluate_word(agent, word)
        results.append(result)
        status = "✅" if result.passed and not result.error else ("💥" if result.error else "❌")
        print(f"{status} {word}")

    print_summary(results)

    if args.output:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "model": config.openai_model,
            "words_tested": len(words),
            "summary": {
                "total": len(results),
                "passed": sum(1 for r in results if r.passed and not r.error),
                "failed": sum(1 for r in results if not r.passed and not r.error),
                "errors": sum(1 for r in results if r.error),
            },
            "results": [asdict(r) for r in results],
        }
        with open(args.output, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\n📄 Results saved to {args.output}")

    return 0 if all(r.passed and not r.error for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
