#!/usr/bin/env bash
set -e
source .venv/bin/activate
python reindex.py --corpus corpus
