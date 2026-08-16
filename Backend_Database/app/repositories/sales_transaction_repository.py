from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.sales_transaction import SalesTransaction
from app.models.product import Product
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.store import Store

from decimal import Decimal

from typing import Optional
from datetime import date

from sqlalchemy import or_
from sqlalchemy import func

# =====================================================
# Get All Sales
# =====================================================

def get_all_sales(

    db: Session,

    page: int = 1,

    page_size: int = 10,

    start_date: Optional[date] = None,

    end_date: Optional[date] = None,

    search: Optional[str] = None,

):

    query = (
        db.query(SalesTransaction)
        .join(Product)
    )

    # ==========================
    # Date Range Filter
    # ==========================

    if start_date:

        query = query.filter(
            SalesTransaction.transaction_date >= start_date
        )

    if end_date:

        query = query.filter(
            SalesTransaction.transaction_date <= end_date
        )

    # ==========================
    # Search
    # ==========================

    if search:

        query = query.filter(

            or_(

                SalesTransaction.transaction_id.ilike(
                    f"%{search}%"
                ),

                SalesTransaction.invoice_id.ilike(
                    f"%{search}%"
                ),

                SalesTransaction.customer_id.ilike(
                    f"%{search}%"
                ),

                SalesTransaction.product_id.ilike(
                    f"%{search}%"
                ),

            )

        )

    sales = (

        query

        .order_by(
            SalesTransaction.transaction_date.desc()
        )

        .offset((page - 1) * page_size)

        .limit(page_size)

        .all()

    )

    for sale in sales:
        sale.product_name = sale.product.product_name
        sale.category = sale.product.category

    return sales


# =====================================================
# Get Sale By Transaction ID
# =====================================================

def get_sale_by_transaction_id(
    db: Session,
    transaction_id: str
):
    sale = (
        db.query(SalesTransaction)
        .join(Product)
        .filter(
            SalesTransaction.transaction_id == transaction_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales transaction not found."
        )

    sale.product_name = sale.product.product_name
    sale.category = sale.product.category

    return sale


# =====================================================
# Create Sale + Reduce Inventory
# =====================================================

def create_sale(
    db: Session,
    sale
):

    # =================================================
    # Validate Product
    # =================================================

    product = (
        db.query(Product)
        .filter(
            Product.product_id == sale.product_id
        )
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    # =================================================
    # Validate Inventory
    # =================================================

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == sale.product_id
        )
        .first()
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found."
        )

    # =================================================
    # Validate Stock
    # =================================================

    if inventory.stock_quantity < sale.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock available."
        )

    # =================================================
    # Get Unit Price From Products Table
    # =================================================

    unit_price = product.unit_price

    # =================================================
    # Calculate Subtotal
    # =================================================

    subtotal = (
        unit_price * sale.quantity
    ).quantize(Decimal("0.01"))

    # =================================================
    # Calculate Discount
    #
    # discount is treated as a percentage
    # =================================================

    discount_amount = (
        subtotal * sale.discount / Decimal("100")
    ).quantize(Decimal("0.01"))

    # =================================================
    # Calculate Final Total
    # =================================================

    total_amount = (
        subtotal - discount_amount
    ).quantize(Decimal("0.01"))

    # =================================================
    # Reduce Inventory
    # =================================================

    inventory.stock_quantity -= sale.quantity

    # =================================================
    # Create Sales Transaction
    # =================================================

    new_sale = SalesTransaction(
        transaction_id=sale.transaction_id,
        invoice_id=sale.invoice_id,
        transaction_date=sale.transaction_date,
        customer_id=sale.customer_id,
        product_id=sale.product_id,
        store_id=sale.store_id,
        quantity=sale.quantity,
        unit_price=unit_price,
        discount=sale.discount,
        total_amount=total_amount,
        payment_method=sale.payment_method,
        created_by_user_id=sale.created_by_user_id
    )

    db.add(new_sale)

    # =================================================
    # Commit
    # =================================================

    db.commit()

    db.refresh(new_sale)

    # =================================================
    # Add Product Information For Response
    # =================================================

    new_sale.product_name = product.product_name
    new_sale.category = product.category

    return new_sale


# =====================================================
# Update Sale
# =====================================================

def update_sale(
    db: Session,
    transaction_id: str,
    updated_sale
):
    # Find existing sale
    sale = (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.transaction_id == transaction_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales transaction not found."
        )

    # Find product
    product = (
        db.query(Product)
        .filter(
            Product.product_id == sale.product_id
        )
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    # Find inventory
    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == sale.product_id
        )
        .first()
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found."
        )

    # New values
    new_quantity = (
        updated_sale.quantity
        if updated_sale.quantity is not None
        else sale.quantity
    )

    new_discount = (
        updated_sale.discount
        if updated_sale.discount is not None
        else sale.discount
    )

    if new_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero."
        )

    if new_discount < 0 or new_discount > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discount must be between 0 and 100."
        )

    # Calculate quantity difference
    quantity_difference = new_quantity - sale.quantity

    # Update inventory
    if quantity_difference > 0:

        if inventory.stock_quantity < quantity_difference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock available."
            )

        inventory.stock_quantity -= quantity_difference

    elif quantity_difference < 0:

        inventory.stock_quantity += abs(quantity_difference)

    # Get authoritative price
    unit_price = product.unit_price

    # Calculate total
    subtotal = (
        unit_price * new_quantity
    ).quantize(Decimal("0.01"))

    discount_amount = (
        subtotal * new_discount / Decimal("100")
    ).quantize(Decimal("0.01"))

    total_amount = (
        subtotal - discount_amount
    ).quantize(Decimal("0.01"))

    # Update sale
    sale.quantity = new_quantity
    sale.unit_price = unit_price
    sale.discount = new_discount
    sale.total_amount = total_amount

    if updated_sale.payment_method is not None:
        sale.payment_method = updated_sale.payment_method

    # Explicitly tell SQLAlchemy both objects changed
    db.add(inventory)
    db.add(sale)

    db.commit()

    db.refresh(inventory)
    db.refresh(sale)

    # Response fields
    sale.product_name = product.product_name
    sale.category = product.category

    return sale


# =====================================================
# Delete Sale
# =====================================================

def delete_sale(
    db: Session,
    transaction_id: str
):

    sale = (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.transaction_id == transaction_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales transaction not found."
        )

    db.delete(sale)

    db.commit()

    return {
        "message": "Sales transaction deleted successfully."
    }


# =====================================================
# Bulk Sales CSV Import
# =====================================================

def bulk_import_sales(
    db: Session,
    dataframe
):

    inserted_count = 0
    skipped_count = 0
    created_invoice_count = 0
    created_item_count = 0

    try:

        # -------------------------------------------------
        # Process invoices order-by-order
        # -------------------------------------------------

        invoice_groups = dataframe.groupby(
            "invoice_id",
            sort=False
        )

        for invoice_id, invoice_rows in invoice_groups:

            invoice_id = str(invoice_id)

            first_row = invoice_rows.iloc[0]

            # ---------------------------------------------
            # Check customer consistency within order
            # ---------------------------------------------

            customer_ids = (
                invoice_rows["customer_id"]
                .astype(str)
                .unique()
            )

            if len(customer_ids) != 1:

                raise HTTPException(
                    status_code=400,
                    detail={
                        "message":
                            "Multiple customers found "
                            "for the same invoice.",
                        "invoice_id":
                            invoice_id
                    }
                )

            customer_id = customer_ids[0]

            # ---------------------------------------------
            # Check store consistency within order
            # ---------------------------------------------

            store_ids = (
                invoice_rows["store_id"]
                .astype(str)
                .unique()
            )

            if len(store_ids) != 1:

                raise HTTPException(
                    status_code=400,
                    detail={
                        "message":
                            "Multiple stores found "
                            "for the same invoice.",
                        "invoice_id":
                            invoice_id
                    }
                )

            store_id = store_ids[0]

            # ---------------------------------------------
            # Validate customer
            # ---------------------------------------------

            customer = (
                db.query(Customer)
                .filter(
                    Customer.customer_id
                    == customer_id
                )
                .first()
            )

            if not customer:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Customer not found: "
                        f"{customer_id}"
                    )
                )

            # ---------------------------------------------
            # Validate store
            # ---------------------------------------------

            store = (
                db.query(Store)
                .filter(
                    Store.store_id
                    == store_id
                )
                .first()
            )

            if not store:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Store not found: "
                        f"{store_id}"
                    )
                )

            # ---------------------------------------------
            # Validate user
            # ---------------------------------------------

            user_id = int(
                first_row["created_by_user_id"]
            )

            # ---------------------------------------------
            # Calculate invoice totals
            # ---------------------------------------------

            subtotal = Decimal("0.00")
            discount_amount = Decimal("0.00")
            total_amount = Decimal("0.00")

            for _, row in invoice_rows.iterrows():

                subtotal += Decimal(
                    str(row["unit_price"])
                ) * int(row["quantity"])

                discount_amount += Decimal(
                    str(row["discount"])
                )

                total_amount += Decimal(
                    str(row["total_amount"])
                )

            # ---------------------------------------------
            # Find existing invoice
            # ---------------------------------------------

            invoice = (
                db.query(Invoice)
                .filter(
                    Invoice.invoice_id
                    == invoice_id
                )
                .first()
            )

            # ---------------------------------------------
            # Create invoice if necessary
            # ---------------------------------------------

            if not invoice:

                invoice = Invoice(
                    invoice_id=invoice_id,
                    invoice_number=invoice_id,
                    customer_id=customer_id,
                    store_id=store_id,
                    created_by_user_id=user_id,
                    invoice_date=first_row[
                        "transaction_date"
                    ],
                    due_date=first_row[
                        "transaction_date"
                    ],
                    subtotal=subtotal,
                    discount_amount=discount_amount,
                    tax_amount=Decimal("0.00"),
                    total_amount=total_amount,
                    payment_status="Unknown",
                    invoice_status="Imported",
                    notes="Imported from sales CSV"
                )

                db.add(invoice)

                db.flush()

                created_invoice_count += 1

            # ---------------------------------------------
            # Process individual sales rows
            # ---------------------------------------------

            for _, row in invoice_rows.iterrows():

                transaction_id = str(
                    row["transaction_id"]
                )

                # -----------------------------------------
                # Skip duplicate transaction
                # -----------------------------------------

                existing_sale = (
                    db.query(SalesTransaction)
                    .filter(
                        SalesTransaction.transaction_id
                        == transaction_id
                    )
                    .first()
                )

                if existing_sale:

                    skipped_count += 1
                    continue

                # -----------------------------------------
                # Validate product
                # -----------------------------------------

                product = (
                    db.query(Product)
                    .filter(
                        Product.product_id
                        == str(row["product_id"])
                    )
                    .first()
                )

                if not product:

                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "Product not found: "
                            f"{row['product_id']}"
                        )
                    )

                quantity = int(
                    row["quantity"]
                )

                unit_price = Decimal(
                    str(row["unit_price"])
                )

                discount = Decimal(
                    str(row["discount"])
                )

                line_total = Decimal(
                    str(row["total_amount"])
                )

                # -----------------------------------------
                # Create invoice item
                # -----------------------------------------

                invoice_item = InvoiceItem(
                    invoice_id=invoice_id,
                    product_id=str(
                        row["product_id"]
                    ),
                    quantity=quantity,
                    unit_price=unit_price,
                    discount=discount,
                    tax=Decimal("0.00"),
                    line_total=line_total,
                    category_snapshot=(
                        product.category
                    ),
                    product_name_snapshot=(
                        product.product_name
                    )
                )

                db.add(invoice_item)

                created_item_count += 1

                # -----------------------------------------
                # Create sales transaction
                # -----------------------------------------

                sale = SalesTransaction(
                    transaction_id=transaction_id,
                    invoice_id=invoice_id,
                    transaction_date=row[
                        "transaction_date"
                    ],
                    customer_id=customer_id,
                    product_id=str(
                        row["product_id"]
                    ),
                    store_id=store_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    discount=discount,
                    total_amount=line_total,
                    payment_method=str(
                        row["payment_method"]
                    ),
                    created_by_user_id=user_id
                )

                db.add(sale)

                inserted_count += 1

        # -------------------------------------------------
        # One atomic commit
        # -------------------------------------------------

        db.commit()

        return {
            "inserted_count": inserted_count,
            "skipped_count": skipped_count,
            "created_invoice_count":
                created_invoice_count,
            "created_item_count":
                created_item_count,
        }

    except HTTPException:

        db.rollback()
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Sales CSV import failed: "
                f"{str(e)}"
            )
        )
