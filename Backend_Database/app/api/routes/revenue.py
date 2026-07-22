from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.revenue import RevenueSummaryResponse

from app.services.revenue_service import (
    get_revenue_summary,
)

router = APIRouter(
    prefix="/revenue",
    tags=["Revenue Summary"]
)


# =====================================================
# Revenue Summary
# =====================================================

@router.get(
    "/summary",
    response_model=RevenueSummaryResponse
)
def revenue_summary(
    db: Session = Depends(get_db)
):

    return get_revenue_summary(db)
