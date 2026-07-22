from sqlalchemy.orm import Session
from app.models.invoice_item import InvoiceItem


def get_items_by_invoice(
    db: Session,
    invoice_id: str
):

    return (
        db.query(InvoiceItem)
        .filter(
            InvoiceItem.invoice_id == invoice_id
        )
        .all()
    )

def add_invoice_item(
    db: Session,
    item_data: dict
):

    new_item = InvoiceItem(**item_data)

    db.add(new_item)

    db.commit()

    db.refresh(new_item)

    return new_item

def delete_invoice_items(
    db: Session,
    invoice_id: str
):

    items = (
        db.query(InvoiceItem)
        .filter(
            InvoiceItem.invoice_id == invoice_id
        )
        .all()
    )

    for item in items:
        db.delete(item)

    db.commit()

    return {
        "message": "Invoice items deleted successfully."
    }
