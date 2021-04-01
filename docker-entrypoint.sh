#!/bin/bash
# Start the API server
echo "Starting the API server v2"
exec poetry run uvicorn instances_management.main:app --host 0.0.0.0 --log-level debug --reload
