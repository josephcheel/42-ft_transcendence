#!/bin/sh

while [ ! -f ./.migration_done ]; do
  sleep 1
done

python manage.py runserver 0.0.0.0:8000
