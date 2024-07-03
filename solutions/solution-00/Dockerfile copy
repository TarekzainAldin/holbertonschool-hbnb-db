# Use the latest slim version of Python 3.12
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Copy the rest of the application code
COPY . .

# Environment variables
ENV PORT 5000

# Expose the port
EXPOSE $PORT

# Run the application
CMD ["gunicorn", "hbnb:app", "-w", "2", "-b", "0.0.0.0:$PORT"]
