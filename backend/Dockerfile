# Stage 1: Build
FROM python:3.11 as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory for the build stage
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv

# Set PATH to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install  -r requirements.txt
    

COPY . .

# Stage 2: Runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory for the runtime stage
WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Set PATH to use the virtual environment in runtime as well
ENV PATH="/opt/venv/bin:$PATH"

# Add the current directory to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"


EXPOSE 8000

