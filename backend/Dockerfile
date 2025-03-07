FROM python:3.11-slim

# Install system dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
COPY pip.conf /root/.pip/pip.conf

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create migrations directory if it doesn't exist
RUN mkdir -p migrations/versions

# Run migrations and start the application
CMD alembic upgrade head && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload