#!/usr/bin/env bash

echo "Installing project requierements..."
pip install -r requirements.txt

echo "Collecting static files..." 
python3 manage.py collectstatic --no-input