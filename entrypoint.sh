#!/bin/bash

# Collect static files
echo "Collect static files"
python /nominate_ur_bee/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python /nominate_ur_bee/manage.py migrate

# Start server
echo "Starting server"
python /nominate_ur_bee/manage.py runserver 0.0.0.0:3003