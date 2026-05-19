#!/usr/bin/env python3
"""Scan tracked files for public-safety issues before commit/CI."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path("scripts/check_public_safety.py")

TEXT_EXTENSIONS = {
    ".ipynb",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".sql",
    ".txt",
    ".yaml",
    ".yml",
}

BLOCKED_FILE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
BLOCKED_FILE_NAMES = {".env"}

PATTERNS = [
    (
        "databricks_workspace_host",
        re.compile(r"https://adb-\d+\.\d+\.azuredatabricks\.net"),
        "Replace real Databricks workspace hosts with https://<your-workspace-host>.",
    ),
    (
        "databricks_workspace_id",
        re.compile(r"adb-\d+"),
        "Do not commit concrete Databricks workspace IDs.",
    ),
    (
        "local_user_path",
        re.compile(r"/Users/[A-Za-z0-9._-]+/"),
        "Replace local absolute paths with ${REPO_ROOT}/... or /path/to/repo/...",
    ),
    (
        "email_address",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "Avoid committing private email addresses; use generic placeholders.",
    ),
    (
        "secret_assignment",
        re.compile(
            r"(?i)\b(api[_-]?key|client[_-]?secret|secret|token|password)\b\s*[:=]\s*['\"]?[^'\"\s]+"
        ),
        "Do not commit credentials or credential-like assignments.",
    ),
]


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(item) for item in result.stdout.decode("utf-8").split("\0") if item]


def optional_denylist() -> list[tuple[str, re.Pattern[str], str]]:
    denylist_path = ROOT / ".public_safety_denylist"
    if not denylist_path.exists():
        return []

    patterns: list[tuple[str, re.Pattern[str], str]] = []
    for index, line in enumerate(denylist_path.read_text(encoding="utf-8").splitlines(), start=1):
        term = line.strip()
        if not term or term.startswith("#"):
            continue
        patterns.append(
            (
                f"local_denylist_{index}",
                re.compile(re.escape(term), re.IGNORECASE),
                "A term from .public_safety_denylist appears in tracked content.",
            )
        )
    return patterns


def read_text(path: Path) -> str | None:
    full_path = ROOT / path
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return None
    try:
        return full_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def main() -> int:
    errors: list[str] = []
    patterns = PATTERNS + optional_denylist()

    for path in tracked_files():
        if path == SELF:
            continue

        name = path.name.lower()
        suffix = path.suffix.lower()
        if name in BLOCKED_FILE_NAMES or suffix in BLOCKED_FILE_EXTENSIONS:
            errors.append(f"{path}: tracked file type is not public-safe for this repo.")
            continue

        text = read_text(path)
        if text is None:
            continue

        for pattern_name, pattern, message in patterns:
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                preview = match.group(0)
                errors.append(f"{path}:{line_no}: {pattern_name}: {preview!r}. {message}")

    if errors:
        print("Public-safety check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Public-safety check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
