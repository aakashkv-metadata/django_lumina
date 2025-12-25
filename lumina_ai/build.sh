#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
# We use 'backend/manage.py' assuming we are in 'lumina_ai' directory
python backend/manage.py collectstatic --no-input

# Apply database migrations
python backend/manage.py migrate
