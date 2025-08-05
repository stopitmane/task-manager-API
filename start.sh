#!/bin/bash

# Get the port from environment variable or default to 8000
PORT=${PORT:-8000}

echo "Starting Task Management System API on port $PORT"

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT 