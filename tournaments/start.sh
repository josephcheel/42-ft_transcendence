#!/bin/sh

chmod +x ./wait_for_it.sh
./wait_for_it.sh ${DB_HOST}:${DB_PORT} --timeout=0

python manage.py makemigrations
python manage.py migrate tournamentsapp
python manage.py runserver 0.0.0.0:8000
 
