#!/bin/bash

# Start the FastAPI backend
echo "Starting FastAPI backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start the React frontend development server
echo "Starting React frontend..."
cd frontend && npm start &
FRONTEND_PID=$!

# Function to handle cleanup
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID