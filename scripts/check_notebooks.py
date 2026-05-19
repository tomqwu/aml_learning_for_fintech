#!/usr/bin/env python3
"""Validate checked-in notebook examples without requiring Spark."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source_text(source: object) -> str:
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    if isinstance(source, str):
        return source
    return ""


def python_compile_text(source: str) -> str:
    """Drop notebook magic lines before Python syntax validation."""
    python_lines: list[str] = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("%") or stripped.startswith("!"):
            continue
        python_lines.append(line)
    return "\n".join(python_lines) + "\n"


def validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if notebook.get("nbformat") != 4:
        errors.append(f"{path}: expected nbformat 4")

    cells = notebook.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append(f"{path}: expected non-empty cells list")
        return errors

    markdown_count = 0
    code_count = 0

    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            errors.append(f"{path}: cell {index} is not an object")
            continue

        cell_type = cell.get("cell_type")
        text = source_text(cell.get("source"))

        if cell_type == "markdown":
            markdown_count += 1
            if not text.strip():
                errors.append(f"{path}: markdown cell {index} is empty")
        elif cell_type == "code":
            code_count += 1
            previous_cell = cells[index - 2] if index > 1 else None
            previous_text = source_text(previous_cell.get("source")) if isinstance(previous_cell, dict) else ""
            if (
                not isinstance(previous_cell, dict)
                or previous_cell.get("cell_type") != "markdown"
                or "**Code-cell explanation:**" not in previous_text
            ):
                errors.append(
                    f"{path}: code cell {index} must be preceded by markdown with "
                    "'**Code-cell explanation:**'"
                )
            try:
                compile(python_compile_text(text), f"{path}:cell-{index}", "exec")
            except SyntaxError as exc:
                errors.append(f"{path}: Python syntax error in code cell {index}: {exc}")
        else:
            errors.append(f"{path}: cell {index} has unsupported type {cell_type!r}")

    if markdown_count == 0:
        errors.append(f"{path}: expected at least one markdown cell")
    if code_count == 0:
        errors.append(f"{path}: expected at least one code cell")

    return errors


def main() -> int:
    notebooks = sorted((ROOT / "examples").rglob("*.ipynb"))
    if not notebooks:
        print("No notebook examples found.")
        return 0

    errors: list[str] = []
    for notebook in notebooks:
        errors.extend(validate_notebook(notebook))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Notebook check passed ({len(notebooks)} notebook(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
