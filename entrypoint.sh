#!/bin/bash

# Collect static files
echo "Collect static files"
python /nominate_ur_bee/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python /nominate_ur_bee/manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python /nominate_ur_bee/manage.py migrate

echo "running celery in daemon"
celery -A nominate_your_bee beat --detach -l info -f beat.log
celery -A nominate_your_bee worker --detach -l info -f worker.log

#Apply the default seed to the application
python /nominate_ur_bee/manage.py assign_groups

# Start server
echo "Starting server"
python /nominate_ur_bee/manage.py runserver 0.0.0.0:3003