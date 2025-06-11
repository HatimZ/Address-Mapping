#!/bin/bash

# Start nginx in the background
nginx

# Start the backend server
cd /app/backend
uvicorn src.main:app --host 127.0.0.1 --port 8000 