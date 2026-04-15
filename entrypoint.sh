#!/bin/sh
set -e

if [ -f /app/manage.py ]; then
  python /app/manage.py migrate --noinput
  python /app/manage.py collectstatic --noinput --clear
fi

exec "$@"
