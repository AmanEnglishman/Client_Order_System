#!/bin/bash
set -e

# Check if migrations are needed
echo "Checking database status..."
python manage.py showmigrations --plan | grep -q "\[ \]" && {
    echo "Running migrations..."
    python manage.py migrate
} || echo "No migrations needed."

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"
