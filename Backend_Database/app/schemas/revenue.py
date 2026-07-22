from decimal import Decimal

from pydantic import BaseModel


# =====================================================
# Revenue Summary Response
# =====================================================

class RevenueSummaryResponse(BaseModel):

    total_revenue: Decimal

    total_outstanding: Decimal

    daily_collections: Decimal
