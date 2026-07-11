FROM python:3.11-slim

WORKDIR /app

# Install compilation tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install packages manually since requirements is not in repository
RUN pip install --no-cache-dir flask pandas numpy joblib lightgbm scikit-learn

# Copy AI model and stub code. Keep the stub_service folder name so
# app.py can load stub_service/lightgbm_daily_model.pkl consistently.
COPY ["AIML/week 1/stub_service/", "./stub_service/"]

# Expose Flask port inside container
EXPOSE 5000

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=stub_service/app.py

# Run flask server on all interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
