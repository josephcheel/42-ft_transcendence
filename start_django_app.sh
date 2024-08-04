#!/bin/sh

python manage.py makemigrations $APP

python manage.py migrate $APP

python manage.py runserver 0.0.0.0:8000
