#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default values if not provided
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-INFO}

# Run the application
echo "Starting FastAPI Health Check Microservice..."
echo "Host: $HOST"
echo "Port: $PORT"
echo "Log Level: $LOG_LEVEL"

uvicorn app.main:app --host $HOST --port $PORT --log-level $LOG_LEVEL --reload