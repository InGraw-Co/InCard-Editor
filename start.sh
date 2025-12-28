#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".venv/bin/activate" ]; then
  . .venv/bin/activate
  PYTHON="${PYTHON:-python}"
else
  if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON=python
  else
    echo "Error: Python is not installed. Install Python 3 and try again." >&2
    exit 1
  fi
fi

exec "$PYTHON" -B main.py "$@"
