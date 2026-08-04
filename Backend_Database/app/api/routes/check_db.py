from app.models import SalesTransaction
from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import SessionLocal

router = APIRouter()


@router.get("/check-db")
def check_database():

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
