#!/bin/bash

# Stop on first error
set -o errexit
# Print each command ran
set -o xtrace

case "$SERVICE_NAME" in
producer)
    python -u src/producer_service_main.py --video_file /opt/code/data/traffic.mp4 --log_folder /opt/logs
    ;;
image_processor)
    python -u src/image_processing_service_main.py --log_folder /opt/logs
    ;;
stats_reporter)
    python -u src/stats_reporting_service_main.py
    ;;
*)
    echo "Unknown service name!"
    exit 1
    ;;
esac
