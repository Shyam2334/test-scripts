#!/bin/bash
# Ensure virtual environment is activated
if [ -d "venv" ]; then
    source venv/bin/activate
fi
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload