#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtualenv if present
if [ -d ".venv" ]; then
    export PATH="$SCRIPT_DIR/.venv/bin:$PATH"
fi

# Auto-generate graph + vector artifacts if missing.
if [ ! -f "data/graph.gml" ] || [ ! -f "data/chunks.json" ]; then
    echo "[setup] Generating graph and vector data..."
    python3 generate_data.py
    echo "[setup] Data generation complete."
fi

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

exec uvicorn main:app --host "$HOST" --port "$PORT"
