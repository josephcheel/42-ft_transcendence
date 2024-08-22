#!/bin/sh

set -e

# Loop through each folder in the /app directory

python usermanagement/manage.py makemigrations UserModel
python usermanagement/manage.py migrate

echo "All migrations completed successfully."
