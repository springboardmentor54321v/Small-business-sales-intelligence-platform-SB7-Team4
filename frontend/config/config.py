import os

# Central Config for Frontend APIs
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "http://localhost:5000")      # Local API Gateway
DB_BASE_URL = os.getenv("DB_BASE_URL", "http://localhost:8000")     # Local Database Backend
