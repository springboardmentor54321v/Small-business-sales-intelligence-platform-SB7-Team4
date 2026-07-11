FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for postgres and scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY Backend_Database/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY Backend_Database/ .

# Expose backend API port
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Run Database Backend process
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
