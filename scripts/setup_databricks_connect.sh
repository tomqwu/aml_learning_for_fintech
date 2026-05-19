#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${DATABRICKS_CONNECT_VERSION:-}" ]]; then
  cat >&2 <<'EOF'
Set DATABRICKS_CONNECT_VERSION to the Databricks Runtime major.minor version.

Example:
  PYTHON_BIN=/opt/homebrew/bin/python3.12 \
  DATABRICKS_CONNECT_VERSION=17.3 \
  bash scripts/setup_databricks_connect.sh
EOF
  exit 64
fi

PYTHON_BIN="${PYTHON_BIN:-python3.12}"
VENV_DIR="${VENV_DIR:-.venv-databricks-connect}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python binary not found: $PYTHON_BIN" >&2
  echo "Install the Python version required by your Databricks Connect version, then rerun." >&2
  exit 127
fi

PYTHON_MINOR="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
EXPECTED_PYTHON_MINOR=""

case "$DATABRICKS_CONNECT_VERSION" in
  13.3*|14.3*)
    EXPECTED_PYTHON_MINOR="3.10"
    ;;
  15.4*)
    EXPECTED_PYTHON_MINOR="3.11"
    ;;
  16.4*|17.2*|17.3*|18.*)
    EXPECTED_PYTHON_MINOR="3.12"
    ;;
esac

if [[ -n "$EXPECTED_PYTHON_MINOR" && "$PYTHON_MINOR" != "$EXPECTED_PYTHON_MINOR" ]]; then
  cat >&2 <<EOF
Python version mismatch.

Databricks Connect ${DATABRICKS_CONNECT_VERSION} expects Python ${EXPECTED_PYTHON_MINOR}.
Selected Python binary: ${PYTHON_BIN}
Selected Python version: ${PYTHON_MINOR}

Rerun with a matching Python binary, for example:
  PYTHON_BIN=python${EXPECTED_PYTHON_MINOR} DATABRICKS_CONNECT_VERSION=${DATABRICKS_CONNECT_VERSION} bash scripts/setup_databricks_connect.sh
EOF
  exit 65
fi

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip

echo "Using Python: $("$VENV_DIR/bin/python" --version)"
echo "Checking databricks-connect package visibility for this interpreter..."
"$VENV_DIR/bin/python" -m pip index versions databricks-connect | sed -n '1,2p'

if "$VENV_DIR/bin/python" -m pip show pyspark >/dev/null 2>&1; then
  "$VENV_DIR/bin/python" -m pip uninstall -y pyspark
fi

if ! "$VENV_DIR/bin/python" -m pip install --upgrade \
    "databricks-connect==${DATABRICKS_CONNECT_VERSION}.*" \
    ipykernel; then
  cat >&2 <<EOF

Failed to install databricks-connect==${DATABRICKS_CONNECT_VERSION}.*

Common causes:
  1. VS Code or pip is still using the wrong interpreter.
  2. The selected Python version is not supported for this Databricks Connect version.
  3. A corporate/private package index is hiding newer databricks-connect versions.

Debug:
  ${VENV_DIR}/bin/python --version
  ${VENV_DIR}/bin/python -m pip index versions databricks-connect | head

If the available version list stops at 16.1.7 while installing 17.3,
you are probably using Python 3.14 or another unsupported interpreter.
EOF
  exit 66
fi

"$VENV_DIR/bin/python" - <<'PY'
from importlib import metadata

print("databricks-connect", metadata.version("databricks-connect"))
PY

cat <<EOF

Databricks Connect environment is ready.

Virtual environment:
  ${VENV_DIR}

Interpreter for VS Code / Databricks extension:
  ${PWD}/${VENV_DIR}/bin/python

Next:
  1. Select that interpreter in VS Code.
  2. Authenticate with the Databricks extension or Databricks CLI.
  3. Re-run the Databricks Connect setup / validation.
EOF
