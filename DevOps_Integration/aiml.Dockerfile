# ============================================================
# MarketMind AI - AI/ML Real-Time Analytics Service Dockerfile
# Milestone 4 Production Zero-Cost Deployment
# ============================================================
FROM python:3.11-slim

WORKDIR /app

# Install system compilation packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY AIML/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the full AIML package and model artifacts
COPY AIML/ /app/AIML/

# Configure environment
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV HOST=0.0.0.0

EXPOSE 5000

# Health check probe
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the Flask API service
CMD ["python", "AIML/Integrated_API/app.py"]
