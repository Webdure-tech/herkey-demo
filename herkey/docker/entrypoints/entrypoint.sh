#!/bin/sh

echo "Entrypoint script executed"
python manage.py makemigrations
python manage.py migrate
# python manage.py test

exec "$@"