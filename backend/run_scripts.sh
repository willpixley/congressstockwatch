#!/bin/bash

# Define paths
VENV_PATH="/home/ubuntu/stocktracker-backend/venv"
SCRIPT_PATH="/home/ubuntu/stocktracker-backend/daily_trade_updates.py"
LOG_FILE="/home/ubuntu/stocktracker-backend/logs/trade_updates.log"
DJANGO_PROJECT_PATH="/home/ubuntu/stocktracker-backend/project"
DJANGO_SETTINGS_MODULE="project.settings"  # Adjust this as needed

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Export Django settings module
export DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"

# Run the script and append output to the log file
python "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1
