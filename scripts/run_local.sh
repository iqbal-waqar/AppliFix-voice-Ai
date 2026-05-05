#!/bin/bash
# Run the backend locally
cd "$(dirname "$0")/.."

echo "🚀 Starting Voice AI Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
