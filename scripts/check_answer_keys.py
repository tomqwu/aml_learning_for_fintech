#!/usr/bin/env python3
"""Ensure drill-heavy learning docs include inline answer guidance."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIR_PARTS = {".git", "node_modules"}
ANSWER_KEY_FILE = Path("docs/16-model-answer-bank.md")

TRIGGER_PATTERNS = [
    re.compile(r"^## .*active recall questions", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^## .*closed-book", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^## .*retrieval check", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^# .*practice lab", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^answer without looking:", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^answer and code without looking:", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^answer these without looking\.", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^answer without running code first:", re.IGNORECASE | re.MULTILINE),
]

ANSWER_KEY_MARKERS = [
    "Model answers:",
    "Model answer:",
    "### Model answers",
    "### Model answer",
    "Model answer shape:",
    "Answer standard:",
    "Expected answer:",
    "Expected response:",
    "Expected summary:",
]

LINK_ONLY_PATTERNS = [
    re.compile(r"Model answers?:\s*\[[^\]]+\]\([^)]*16-model-answer-bank\.md[^)]*\)"),
    re.compile(r"Answer key:\s*\[[^\]]+\]\([^)]*16-model-answer-bank\.md[^)]*\)"),
    re.compile(r"Model answer shape:\s*\[[^\]]+\]\([^)]*16-model-answer-bank\.md[^)]*\)"),
]


def is_ignored(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return any(part in IGNORED_DIR_PARTS or part.startswith(".venv") for part in parts)


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if path.is_file() and not is_ignored(path)
    )


def has_trigger(text: str) -> bool:
    return any(pattern.search(text) for pattern in TRIGGER_PATTERNS)


def has_answer_key_marker(text: str) -> bool:
    return any(marker in text for marker in ANSWER_KEY_MARKERS)


def has_link_only_answer_key(text: str) -> bool:
    return any(pattern.search(text) for pattern in LINK_ONLY_PATTERNS)


def main() -> int:
    errors: list[str] = []
    for path in markdown_files():
        rel = path.relative_to(ROOT)
        if rel == ANSWER_KEY_FILE:
            continue

        text = path.read_text(encoding="utf-8")
        if has_link_only_answer_key(text):
            errors.append(
                f"{rel}: uses a distant model-answer-bank link instead of inline answers."
            )
        if has_trigger(text) and not has_answer_key_marker(text):
            errors.append(
                f"{rel}: contains drill/retrieval prompts but no inline model-answer or expected-response field."
            )

    if errors:
        print("Answer-key check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Answer-key check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
