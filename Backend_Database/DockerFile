FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY Backend_Database/requirements.txt ./requirements.txt

# Install dependencies
RUN python -c "import re; open('requirements.txt','w').write(re.sub(r'==.*','',open('requirements.txt').read()))" && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend project
COPY Backend_Database/ .

# Expose FastAPI port
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
