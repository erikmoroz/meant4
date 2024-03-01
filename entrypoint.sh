#!/usr/bin/env bash

# Try to connect to PostgreSQL
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"

cd /src/api

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata fixtures/initial.json
python manage.py runserver 0.0.0.0:8282