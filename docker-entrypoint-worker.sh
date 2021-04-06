#!/bin/bash
# Start the API server
echo "Starting worker"
exec poetry run celery -A instances_management worker -l DEBUG -Q $WORKER_NAME
