#!/bin/sh

set -e

# Loop through each folder in the /app directory

python usermanagement/manage.py makemigrations user
python usermanagement/manage.py migrate
#python tournaments/manage.py makemigrations tournaments
#python tournaments/manage.py migrate

echo "All migrations completed successfully."
