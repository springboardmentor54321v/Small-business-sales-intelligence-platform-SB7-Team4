# pyrefly: ignore-file
# type: ignore
import sys
import os

# Set DATABASE_URL to a dummy sqlite path so SQLAlchemy doesn't raise error
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Adjust sys.path to include Backend_Database parent directory
__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), "..", "..", "Backend_Database"))

def test_backend_orm_metadata():
    """Verify backend model table mapping constraints are correct."""
    from app.models import SalesTransaction
    assert SalesTransaction.__tablename__ == "sales_transactions"
    
def test_backend_endpoints_loading():
    """Verify that backend router definitions load cleanly."""
    from app.api.routes.test_db import router
    assert router is not None
