#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate --no-input
DJANGO_SUPERUSER_PASSWORD=password1234 python manage.py createsuperuser \
    --no-input --username=admin --email=admin@test.es
pytest

exec "$@"
