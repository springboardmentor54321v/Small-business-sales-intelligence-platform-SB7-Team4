from sqlalchemy.orm import Session

from app.models.inventory import Inventory

from datetime import date
from app.models.invoice import Invoice


class NotificationRepository:

    @staticmethod
    def get_low_stock_inventory(db: Session):

        return (
            db.query(Inventory)
            .filter(
                Inventory.stock_quantity <= Inventory.low_stock_threshold
            )
            .all()
        )

    @staticmethod
    def get_overdue_invoices(db: Session):

        return (
            db.query(Invoice)
            .filter(
                Invoice.due_date < date.today(),
                Invoice.payment_status.in_(
                    ["Pending", "Partially Paid"]
                )
            )
            .all()
        )
