#!/usr/bin/env python3
"""Guard README files so they remain navigational and public-friendly."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", "node_modules", ".venv"}
ROOT_MAX_LINES = 260
FOLDER_MAX_LINES = 140

FORBIDDEN_PHRASES = {
    "Codex continuation brief": "README files should not contain stale agent handoff notes.",
    "repo was uninitialized": "README files should not preserve obsolete setup state.",
    "Target GitHub repo": "README files should not preserve old handoff metadata.",
    "aml_learning_for_fintech_deep_research_codex_handoff.zip": "README files should not reference obsolete local handoff artifacts.",
    "Initial AML fintech learning pack with Codex handoff": "README files should not include old suggested commit messages.",
}

BARE_PATH_PATTERN = re.compile(
    r"^[A-Za-z0-9_./-]+\.(?:md|ipynb|py|sql|yaml|yml|json|sh)$"
)


def is_ignored(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    if parts & IGNORED_DIRS:
        return True
    return any(part.startswith(".venv-") for part in parts)


def readme_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("README.md")
        if path.is_file() and not is_ignored(path)
    )


def code_blocks(lines: list[str]) -> list[tuple[int, list[str]]]:
    blocks: list[tuple[int, list[str]]] = []
    in_block = False
    start_line = 0
    current: list[str] = []

    for idx, line in enumerate(lines, start=1):
        if line.startswith("```"):
            if not in_block:
                in_block = True
                start_line = idx
                current = []
            else:
                blocks.append((start_line, current))
                in_block = False
            continue
        if in_block:
            current.append(line.rstrip("\n"))

    return blocks


def check_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    max_lines = ROOT_MAX_LINES if rel == Path("README.md") else FOLDER_MAX_LINES
    if len(lines) > max_lines:
        errors.append(f"{rel}: has {len(lines)} lines; README limit is {max_lines}.")

    for phrase, reason in FORBIDDEN_PHRASES.items():
        if phrase in text:
            errors.append(f"{rel}: contains stale phrase {phrase!r}. {reason}")

    for start_line, block_lines in code_blocks(lines):
        meaningful_lines = [line.strip() for line in block_lines if line.strip()]
        if len(meaningful_lines) == 1 and BARE_PATH_PATTERN.match(meaningful_lines[0]):
            errors.append(
                f"{rel}:{start_line}: bare repository path in code block; use a Markdown link instead."
            )

    return errors


def main() -> int:
    errors: list[str] = []
    for path in readme_files():
        errors.extend(check_file(path))

    if errors:
        print("README navigation check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("README navigation check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
