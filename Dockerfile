# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=gym_app.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY req.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r req.txt
RUN pip install gunicorn

# Copy project files
COPY . .

# Change to the directory containing manage.py
WORKDIR /app/gym_app

# Create staticfiles directory
RUN mkdir -p staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server using gunicorn
CMD python manage.py migrate && gunicorn gym_app.wsgi:application --bind 0.0.0.0:8000 