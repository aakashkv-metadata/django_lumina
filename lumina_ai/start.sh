#!/usr/bin/env bash
# Exit on error
set -o errexit

# Navigate to backend directory
cd backend

# Run Gunicorn
# Using exec to replace the shell with the gunicorn process
exec gunicorn lumina.wsgi:application --bind 0.0.0.0:$PORT
