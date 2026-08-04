from sqlalchemy.orm import Session

from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import (
    Notification,
    NotificationListResponse,
    NotificationSeverity,
    NotificationType,
)

from datetime import date

LOW_STOCK_TITLE = "Low Stock Alert"
OVERDUE_INVOICE_TITLE = "Overdue Invoice"


class NotificationService:

    @staticmethod
    def get_inventory_severity(
        stock: int,
        threshold: int,
    ) -> NotificationSeverity:

        if stock <= threshold * 0.25:
            return NotificationSeverity.CRITICAL

        elif stock <= threshold * 0.50:
            return NotificationSeverity.HIGH

        return NotificationSeverity.MEDIUM

    @staticmethod

    def get_invoice_severity(
        due_date: date,
    ) -> NotificationSeverity:

        overdue_days = (
            date.today() - due_date
        ).days

        if overdue_days > 30:
            return NotificationSeverity.CRITICAL

        elif overdue_days > 7:
            return NotificationSeverity.HIGH

        return NotificationSeverity.MEDIUM

    @staticmethod
    def get_notifications(
        db: Session,
    ) -> NotificationListResponse:

        inventory_items = (
            NotificationRepository.get_low_stock_inventory(db)
        )

        notifications = []

        # ==========================
        # Low Stock Notifications
        # ==========================

        for item in inventory_items:

            severity = NotificationService.get_inventory_severity(
                item.stock_quantity,
                item.low_stock_threshold,
            )

            notifications.append(
                Notification(
                    type=NotificationType.LOW_STOCK,
                    severity=severity,
                    title=LOW_STOCK_TITLE,
                    message=(
                        f"Product {item.product_id} has only "
                        f"{item.stock_quantity} units remaining."
                    ),
                    reference_id=item.product_id,
                )
            )

        # ==========================
        # Overdue Invoice Notifications
        # ==========================

        overdue_invoices = (
            NotificationRepository.get_overdue_invoices(db)
        )

        for invoice in overdue_invoices:
            overdue_days = (date.today() - invoice.due_date).days
            notifications.append(
                Notification(
                    type=NotificationType.OVERDUE_INVOICE,
                    severity=NotificationService.get_invoice_severity(
                        invoice.due_date
                    ),
                    title=OVERDUE_INVOICE_TITLE,
                    overdue_days=overdue_days,
                    message=(
                        f"Invoice {invoice.invoice_number} "
                        f"is overdue by {overdue_days} days."
                    ),
                    reference_id=invoice.invoice_id,
                )
            )

        return NotificationListResponse(
            total_notifications=len(notifications),
            notifications=notifications,
        )
