#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (Unfold UI, custom CSS/JS)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate