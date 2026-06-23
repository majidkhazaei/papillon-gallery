#!/bin/sh

echo "Waiting for DB..."

while ! nc -z db 5432; do
  sleep 1
done

echo "DB ready!"

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn config.wsgi:application --bind 0.0.0.0:8000
