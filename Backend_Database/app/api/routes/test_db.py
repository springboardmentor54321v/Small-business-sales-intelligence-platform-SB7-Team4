from app.models import SalesTransaction
from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import SessionLocal

router = APIRouter()


@router.get("/test-db")
def test_database():

    db = SessionLocal()

    try:
        count = db.query(SalesTransaction).count()

        return {
            "status": "success",
            "message": "SQLAlchemy ORM connected successfully!",
            "sales_transactions": count
        }

    finally:
        db.close()
