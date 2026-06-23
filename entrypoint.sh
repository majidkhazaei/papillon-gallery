#!/bin/sh

echo "Waiting for DB..."

while ! nc -z db 5432; do
  sleep 1
done

echo "DB ready!"


echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis ready!"


python manage.py migrate --noinput
python manage.py collectstatic --noinput


gunicorn A.wsgi:application --bind 0.0.0.0:8000 --workers 3