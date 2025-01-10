# Use the official Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

    # Copy and install Python dependencies
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the application code
    COPY . .

    # Set the entry point
    CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]