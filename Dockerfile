# Use Python 3.10 slim image as the base image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set a working directory inside the container
WORKDIR /e_commerce_restful_api

# Install dependencies in a separate stage to leverage Docker caching
FROM base as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt for installing dependencies
COPY requirements.txt /e_commerce_restful_api/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /e_commerce_restful_api/requirements.txt

# Copy the application files
FROM base as final

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the FastAPI application files into the container
COPY . /e_commerce_restful_api

# Expose the port for FastAPI
EXPOSE 8000

# Start the FastAPI application using uvicorn with production settings
CMD ["uvicorn", "bin.e_commerce:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
