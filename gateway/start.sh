#!/bin/sh
#openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
 # -keyout /app/django-selfsigned.key \
  #-out /app/django-selfsigned.crt \
  #-subj "/C=ES/ST=Barcelona/L=Barcelona/O=Transcendence/OU=Frontend/CN=localhost"
python manage.py runserver 0.0.0.0:8000
#_plus 0.0.0.0:8000 --cert-file /app/django-selfsigned.crt --key-file /app/django-selfsigned.key
 