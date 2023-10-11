#!/bin/bash
set -euo pipefail

if [ -v DEV_MODE ]; then
    alembic upgrade head
    python -m app.initial_data
fi

uvicorn app.main:app --host 0.0.0.0 --port 80
