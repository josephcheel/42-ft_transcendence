#!/bin/sh
python manage.py makemigrations user
python manage.py makemigrations tournamentsapp
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
 
