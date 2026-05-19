#!/usr/bin/env python3
"""Enforce notebook-first policy for runnable Python/Spark SQL examples."""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CODE_LANGS = {"python", "py", "pyspark", "sql"}
MARKER_CONCEPT = "Concept fragment, not runnable alone."
MARKER_NOTEBOOK = "Runnable version:"

# Existing Markdown code fences are grandfathered while the repo migrates
# runnable examples into notebooks. New unmarked fences above this baseline fail.
GRANDFATHERED_UNMARKED_FENCES: dict[str, dict[str, int]] = {
    "docs/01-aml-transaction-monitoring-foundations.md": {"sql": 1},
    "docs/03-rule-migration-spec-as-code.md": {"sql": 1},
    "docs/04-data-quality-reconciliation-defect-management.md": {"sql": 6},
    "docs/06-practice-lab-retrieval-tests.md": {"sql": 1},
    "docs/09-role-data-engineer.md": {"sql": 2},
    "docs/10-role-data-analyst-bi.md": {"sql": 4},
    "docs/spark/first-principles-examples.md": {"python": 17, "sql": 13},
    "docs/spark/pyspark-dataframe-basics-examples.md": {"python": 55},
    "docs/spark/spark-sql-pyspark-deep-learning.md": {"python": 53, "sql": 22},
    "docs/spark/spark-sql-query-basics-examples.md": {"sql": 91},
}


def tracked_markdown_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "*.md"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(item) for item in result.stdout.decode("utf-8").split("\0") if item]


def fenced_blocks(lines: list[str]) -> list[tuple[str, int, int]]:
    blocks: list[tuple[str, int, int]] = []
    in_block = False
    lang = ""
    start = 0

    for idx, line in enumerate(lines, start=1):
        match = re.match(r"^```([^`\s]*)", line)
        if not match:
            continue

        if not in_block:
            in_block = True
            lang = match.group(1).strip().lower()
            start = idx
        else:
            blocks.append((lang, start, idx))
            in_block = False

    return blocks


def is_marked_concept(lines: list[str], start: int, end: int) -> bool:
    window_start = max(0, start - 7)
    window_end = min(len(lines), end + 4)
    context = "\n".join(lines[window_start:window_end])
    return MARKER_CONCEPT in context and MARKER_NOTEBOOK in context


def main() -> int:
    errors: list[str] = []

    for path in tracked_markdown_files():
        rel = path.as_posix()
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
        unmarked_counts: Counter[str] = Counter()
        marked_blocks: list[tuple[str, int]] = []

        for lang, start, end in fenced_blocks(lines):
            if lang not in CODE_LANGS:
                continue
            if is_marked_concept(lines, start, end):
                marked_blocks.append((lang, start))
            else:
                unmarked_counts[lang] += 1

        baseline = defaultdict(int, GRANDFATHERED_UNMARKED_FENCES.get(rel, {}))
        for lang, count in sorted(unmarked_counts.items()):
            allowed = baseline[lang]
            if count > allowed:
                errors.append(
                    f"{rel}: has {count} unmarked {lang} fence(s); allowed grandfathered count is {allowed}."
                )

        if marked_blocks:
            continue

    if errors:
        print("Markdown code policy check failed:")
        print(
            "New Python/PySpark/SQL Markdown fences must either move to a notebook "
            "or be marked as conceptual fragments."
        )
        print(f"Use both markers near the fence: {MARKER_CONCEPT!r} and {MARKER_NOTEBOOK!r}")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Markdown code policy check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
