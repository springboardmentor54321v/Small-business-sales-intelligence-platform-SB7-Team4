from sqlalchemy.orm import Session

from app.repositories.revenue_repository import (
    get_total_revenue,
    get_total_outstanding,
    get_daily_collections,
)

# =====================================================
# Revenue Summary Service
# =====================================================

def get_revenue_summary(
    db: Session
):

    return {
        "total_revenue": get_total_revenue(db),
        "total_outstanding": get_total_outstanding(db),
        "daily_collections": get_daily_collections(db),
    }
