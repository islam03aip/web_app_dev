#!/bin/sh
set -e

until python -c "import os, psycopg; psycopg.connect(host=os.environ['DB_HOST'], port=os.environ.get('DB_PORT', '5432'), user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], dbname=os.environ['DB_NAME']).close()" 2>/dev/null
do
  echo "Waiting for database..."
  sleep 2
done

python manage.py migrate --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-3}"
