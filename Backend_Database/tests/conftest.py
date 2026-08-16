import pytest
from app.core.database import Base, engine
# Import all models to ensure they are registered on Base.metadata
from app.models import (
    Role,
    User,
    Customer,
    Store,
    Product,
    Inventory,
    Invoice,
    InvoiceItem,
    Payment,
    SalesTransaction,
)

@pytest.fixture(scope="session", autouse=True)
def init_db():
    # Create all tables in SQLite
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after test session ends to clean up
    Base.metadata.drop_all(bind=engine)
