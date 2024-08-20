#!/bin/sh

set -e

# Loop through each folder in the /app directory

python usermanagement/manage.py makemigrations users
python usermanagement/manage.py migrate

for dir in /app/*/
do
    # Check if manage.py exists in the directory
    if [ -f "$dir/manage.py" ]; then
        echo "Running migrations for project in $dir..."
        cd "$dir"

        # Get the base name of the project directory
        project_name=$(basename "$dir")

        # Run makemigrations and migrate for each subdirectory (app) that doesn't have the same name as the project
        for subdir in "$dir"*/ 
        do
            app_name=$(basename "$subdir")
            if [ "$app_name" != "$project_name" ]; then
                echo "Running makemigrations and migrate for app: $app_name"
                python manage.py makemigrations "$app_name"
                python manage.py migrate "$app_name"

            else
                echo "Skipping app: $app_name as it matches the project directory name"
            fi
        done

    else
        echo "No manage.py found in $dir, skipping..."
    fi
done

echo "All migrations completed successfully."
