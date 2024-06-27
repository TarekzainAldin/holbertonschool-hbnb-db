# FROM python:3.12.3-slim

# WORKDIR /app

# COPY requirements.txt /tmp/requirements.txt

# RUN pip install --no-cache-dir -r /tmp/requirements.txt \
#   && rm -rf /tmp

# COPY . .

# ENV PORT 5000

# EXPOSE $PORT

# CMD gunicorn hbnb:app -w 2 -b 0.0.0.0:$PORT


# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt separately to leverage Docker caching
COPY requirements.txt /tmp/requirements.txt

# Install system dependencies needed for PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your app runs on
ENV PORT 5000
EXPOSE $PORT

# Command to run the application with Gunicorn
CMD ["gunicorn", "hbnb:app", "-w", "2", "-b", "0.0.0.0:$PORT"]
