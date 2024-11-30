#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install packages
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
