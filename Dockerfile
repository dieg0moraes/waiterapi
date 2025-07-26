# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create a script to run migrations, setup admin, and start server
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python setup_admin.py\n\
python manage.py collectstatic --noinput\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh

RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run the application
CMD ["/app/start.sh"] 