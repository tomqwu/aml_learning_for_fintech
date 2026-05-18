#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash scripts/push_to_github.sh /path/to/aml_learning_for_fintech
#
# This script assumes you have GitHub access configured locally.
# It creates the initial commit for an empty repository or updates main if the repo already exists.

SOURCE_DIR="${1:-$(pwd)}"
REPO_URL="https://github.com/tomqwu/aml_learning_for_fintech.git"
WORK_DIR="/tmp/aml_learning_for_fintech_push"

rm -rf "$WORK_DIR"
git clone "$REPO_URL" "$WORK_DIR"

rsync -av --delete \
  --exclude ".git" \
  --exclude "scripts/push_to_github.sh" \
  "$SOURCE_DIR/" "$WORK_DIR/"

cd "$WORK_DIR"

# If the repository is empty, ensure a main branch exists.
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git checkout -b main
fi

git add .
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "Add AML learning deep research study pack"
git push origin main
