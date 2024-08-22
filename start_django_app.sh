#!/bin/sh


for dir in /app/*/
do
    if [ "$dir" == "usermodel/" ]; then 
        echo "Equal"
        continue 
    fi
    # Check if manage.py exists in the directory
    dir=$(basename "$dir")

    echo "Running migrations for project in $dir..."
    # Get the base name of the project directory
    echo "Running makemigrations and migrate for app: $dir"
    python manage.py makemigrations "$dir"
    python manage.py migrate "$dir"
done
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
