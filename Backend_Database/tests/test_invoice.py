from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.services.invoice_service import (
    calculate_invoice_totals,
)
from app.repositories.invoice_repository import (
    generate_invoice_number,
)


# =====================================================
# Mock Classes
# =====================================================

class MockItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity


class MockProduct:
    def __init__(self):
        self.product_id = "P001"
        self.product_name = "Laptop"
        self.category = "Electronics"
        self.unit_price = Decimal("100.00")


# =====================================================
# Test Invoice Total Calculation
# =====================================================

@patch("app.services.invoice_service.check_inventory")
@patch("app.services.invoice_service.validate_product")
def test_calculate_invoice_totals(
    mock_validate_product,
    mock_check_inventory,
):

    mock_validate_product.return_value = MockProduct()

    items = [
        MockItem("P001", 2)
    ]

    result = calculate_invoice_totals(
        db=MagicMock(),
        items=items,
    )

    assert result["subtotal"] == Decimal("200.00")
    assert result["discount_amount"] == Decimal("0.00")
    assert result["tax_amount"] == Decimal("36.00")
    assert result["total_amount"] == Decimal("236.00")


# =====================================================
# Test First Invoice Number
# =====================================================

def test_generate_invoice_number_first_invoice():

    db = MagicMock()

    query = MagicMock()

    db.query.return_value = query

    query.order_by.return_value.first.return_value = None

    invoice_number = generate_invoice_number(db)

    assert invoice_number == "INV900001"


# =====================================================
# Test Next Invoice Number
# =====================================================

def test_generate_invoice_number_next_invoice():

    db = MagicMock()

    latest_invoice = MagicMock()
    latest_invoice.invoice_number = "INV900025"

    query = MagicMock()

    db.query.return_value = query

    query.order_by.return_value.first.return_value = latest_invoice

    invoice_number = generate_invoice_number(db)

    assert invoice_number == "INV900026"
