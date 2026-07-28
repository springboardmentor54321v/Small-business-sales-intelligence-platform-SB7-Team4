FROM python:3.11-slim

WORKDIR /app

# Install compilation tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Flask manually
RUN pip install --no-cache-dir flask

# Copy notifications app code
COPY ["DevOps_Integration/notifications/", "./"]

# Expose Flask port inside container
EXPOSE 5003

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Run flask server on all interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=5003"]
