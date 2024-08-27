#!/bin/sh

set -e

# Run migrations for User project
echo "Running migrations for User project..."
cd /app/chat
python manage.py makemigrations chatapp
python manage.py migrate chatapp

# Run migrations for Chat project
echo "Running migrations for Chat project..."
cd /app/usermanagement
python manage.py makemigrations users
python manage.py migrate users


# Run migrations for Chat project
echo "Running migrations for Chat project..."
cd /app/tournements
python manage.py makemigrations tournementsapp
python manage.py migrate tournementsapp

echo "Migrations completed successfully."
