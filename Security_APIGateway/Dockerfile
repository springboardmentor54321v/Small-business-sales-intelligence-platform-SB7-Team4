FROM python:3.11-slim

WORKDIR /app

# Install compilation tools for dependencies like bcrypt if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose API Gateway port
EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Run Gateway uvicorn process
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
