from decimal import Decimal
from unittest.mock import patch

from app.services.revenue_service import (
    get_revenue_summary,
)


@patch("app.services.revenue_service.get_daily_collections")
@patch("app.services.revenue_service.get_total_outstanding")
@patch("app.services.revenue_service.get_total_revenue")
def test_get_revenue_summary(
    mock_total_revenue,
    mock_total_outstanding,
    mock_daily_collections,
):

    mock_total_revenue.return_value = Decimal("1000.00")
    mock_total_outstanding.return_value = Decimal("250.00")
    mock_daily_collections.return_value = Decimal("100.00")

    result = get_revenue_summary(db=None)

    assert result["total_revenue"] == Decimal("1000.00")
    assert result["total_outstanding"] == Decimal("250.00")
    assert result["daily_collections"] == Decimal("100.00")
