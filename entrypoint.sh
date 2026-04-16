#!/bin/bash
set -e

# Check if migrations are needed
echo "Checking database status..."
python manage.py showmigrations --plan | grep -q "\[ \]" && {
    echo "Running migrations..."
    python manage.py migrate
} || echo "No migrations needed."

echo "Preparing frontend build..."
mkdir -p /app/frontend_build
if [ -d /app/frontend/build ]; then
  cp -r /app/frontend/build/. /app/frontend_build/ || true
fi

if [ -d /app/frontend/build/static ] && [ -d /app/staticfiles ]; then
  cp -r /app/frontend/build/static/. /app/staticfiles/ || true
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"
