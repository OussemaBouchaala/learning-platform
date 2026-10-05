#!/usr/bin/env bash
# Starts Bench using the ml-fundamentals-lab virtual environment.
cd "$(dirname "$0")"
PY=../ml-fundamentals-lab/.venv/bin/python
[ -x "$PY" ] || PY=python3
exec "$PY" server.py
