#!/usr/bin/env bash
set -euo pipefail

if git grep -nI $'[ \t]$' -- \
  '*.md' \
  '*.yaml' \
  '*.yml' \
  '*.json' \
  '*.jsonc' \
  '*.sql' \
  '*.sh'; then
  echo "Trailing whitespace found. Remove the lines listed above." >&2
  exit 1
fi

echo "Whitespace check passed."
