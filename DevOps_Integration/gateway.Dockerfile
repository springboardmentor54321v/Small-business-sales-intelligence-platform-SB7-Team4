FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for libraries like bcrypt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY Security_APIGateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY Security_APIGateway/ .

# Expose API Gateway port
EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Run Gateway process
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-5000}"]
