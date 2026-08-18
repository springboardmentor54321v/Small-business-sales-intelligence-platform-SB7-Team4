import os

# Central Config for Frontend APIs
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "https://api-gateway-kwnl.onrender.com")      # Your Gateway link (Port 5000)
DB_BASE_URL = os.getenv("DB_BASE_URL", "https://small-business-sales-intelligence.onrender.com")     # Teammate's Database (Port 8000)
