from datetime import date, timedelta

from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationSeverity


# =====================================================
# Inventory Severity Tests
# =====================================================

def test_inventory_severity_critical():

    assert (
        NotificationService.get_inventory_severity(
            stock=5,
            threshold=20,
        )
        == NotificationSeverity.CRITICAL
    )


def test_inventory_severity_high():

    assert (
        NotificationService.get_inventory_severity(
            stock=10,
            threshold=20,
        )
        == NotificationSeverity.HIGH
    )


def test_inventory_severity_medium():

    assert (
        NotificationService.get_inventory_severity(
            stock=18,
            threshold=20,
        )
        == NotificationSeverity.MEDIUM
    )


# =====================================================
# Invoice Severity Tests
# =====================================================

def test_invoice_severity_medium():

    due_date = date.today() - timedelta(days=5)

    assert (
        NotificationService.get_invoice_severity(
            due_date
        )
        == NotificationSeverity.MEDIUM
    )


def test_invoice_severity_high():

    due_date = date.today() - timedelta(days=15)

    assert (
        NotificationService.get_invoice_severity(
            due_date
        )
        == NotificationSeverity.HIGH
    )


def test_invoice_severity_critical():

    due_date = date.today() - timedelta(days=45)

    assert (
        NotificationService.get_invoice_severity(
            due_date
        )
        == NotificationSeverity.CRITICAL
    )
