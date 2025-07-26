#!/bin/bash

# Wait a moment for any file system operations to complete
sleep 2

# Run Django migrations
echo "Running migrations..."
python manage.py migrate

# Set up admin user and sample data
echo "Setting up admin user and sample data..."
python setup_admin.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 