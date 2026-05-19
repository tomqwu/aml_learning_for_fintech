#!/usr/bin/env bash
set -euo pipefail

if ! find examples -name '*.py' -print -quit | grep -q .; then
  echo "No Python examples found."
  exit 0
fi

find examples -name '*.py' -print0 | xargs -0 python -m py_compile
echo "Python example syntax check passed."
