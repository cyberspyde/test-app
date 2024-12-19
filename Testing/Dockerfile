# Use the official Python image
FROM python:3.12.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the default Django port
EXPOSE 8000

# Command to run the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "Testing.asgi:application"]
