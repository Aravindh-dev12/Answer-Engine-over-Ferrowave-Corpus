#!/usr/bin/env bash
set -e
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi
uvicorn app.main:app --host 127.0.0.1 --port 8000
