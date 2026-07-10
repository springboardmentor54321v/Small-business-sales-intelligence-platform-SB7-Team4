import pandas as pd
from pathlib import Path

from app.core.database import SessionLocal

from app.models.customer import Customer
from app.models.product import Product
from app.models.store import Store
from app.models.inventory import Inventory
from app.models.sales_transaction import SalesTransaction

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).parent

OUTPUT_DIR = BASE_DIR / "output"

CUSTOMERS_FILE = OUTPUT_DIR / "customers.csv"
PRODUCTS_FILE = OUTPUT_DIR / "products.csv"
STORES_FILE = OUTPUT_DIR / "stores.csv"
INVENTORY_FILE = OUTPUT_DIR / "inventory.csv"
SALES_FILE = OUTPUT_DIR / "sales_transactions.csv"

# ==========================================
# Database Session
# ==========================================

db = SessionLocal()

print("=" * 60)
print("MarketMind AI - Data Loading")
print("=" * 60)

print("Reading CSV files...")

customers_df = pd.read_csv(CUSTOMERS_FILE)
products_df = pd.read_csv(PRODUCTS_FILE)
stores_df = pd.read_csv(STORES_FILE)
inventory_df = pd.read_csv(INVENTORY_FILE)
sales_df = pd.read_csv(SALES_FILE)

print(f"Customers          : {len(customers_df)}")
print(f"Products           : {len(products_df)}")
print(f"Stores             : {len(stores_df)}")
print(f"Inventory Records  : {len(inventory_df)}")
print(f"Sales Transactions : {len(sales_df)}")

# ==================================================
# Load Customers
# ==================================================

def load_customers():
    print("\n" + "=" * 60)
    print("Loading Customers...")
    print("=" * 60)

    try:

        for _, row in customers_df.iterrows():

            customer = Customer(
                customer_id=row["customer_id"],
                name=row["name"],
                email=row["email"],
                phone=row["phone"]
            )

            db.add(customer)

        db.commit()

        print(f"✓ {len(customers_df)} customers inserted successfully.")

    except Exception as e:

        db.rollback()

        print("Error while loading customers.")
        print(e)

        raise

# ==================================================
# Load Products
# ==================================================

def load_products():

    print("\n" + "=" * 60)
    print("Loading Products...")
    print("=" * 60)

    try:

        for _, row in products_df.iterrows():

            product = Product(
                product_id=row["product_id"],
                product_name=row["product_name"],
                category=row["category"],
                unit_price=row["unit_price"]
            )

            db.add(product)

        db.commit()

        print(f"✓ {len(products_df)} products inserted successfully.")

    except Exception as e:

        db.rollback()

        print("Error while loading products.")
        print(e)

        raise

# ==================================================
# Load Stores
# ==================================================

def load_stores():

    print("\n" + "=" * 60)
    print("Loading Stores...")
    print("=" * 60)

    try:

        for _, row in stores_df.iterrows():

            store = Store(
                store_id=row["store_id"],
                store_name=row["store_name"],
                location=row["location"]
            )

            db.add(store)

        db.commit()

        print(f"✓ {len(stores_df)} stores inserted successfully.")

    except Exception as e:

        db.rollback()

        print("Error while loading stores.")
        print(e)

        raise


# ==================================================
# Load Inventory
# ==================================================

def load_inventory():

    print("\n" + "=" * 60)
    print("Loading Inventory...")
    print("=" * 60)

    try:

        for _, row in inventory_df.iterrows():

            inventory = Inventory(
                product_id=row["product_id"],
                stock_quantity=row["stock_quantity"],
                low_stock_threshold=row["low_stock_threshold"]
            )

            db.add(inventory)

        db.commit()

        print(f"✓ {len(inventory_df)} inventory records inserted successfully.")

    except Exception as e:

        db.rollback()

        print("Error while loading inventory.")
        print(e)

        raise

# ==================================================
# Load Sales Transactions
# ==================================================

def load_sales_transactions():

    print("\n" + "=" * 60)
    print("Loading Sales Transactions...")
    print("=" * 60)

    try:

        for _, row in sales_df.iterrows():

            sale = SalesTransaction(

                transaction_id=row["transaction_id"],

                invoice_id=row["invoice_id"],

                transaction_date=row["transaction_date"],

                customer_id=row["customer_id"],

                product_id=row["product_id"],

                store_id=row["store_id"],

                quantity=row["quantity"],

                unit_price=row["unit_price"],

                discount=row["discount"],

                total_amount=row["total_amount"],

                payment_method=row["payment_method"],

                created_by_user_id=row["created_by_user_id"]

            )

            db.add(sale)

        db.commit()

        print(f"✓ {len(sales_df)} sales transactions inserted successfully.")

    except Exception as e:

        db.rollback()

        print("Error while loading sales transactions.")
        print(e)

        raise
    
# ==================================================
# Main Function
# ==================================================

def main():

    # load_customers()
    # load_products()
    # load_stores()
    # load_inventory()
    load_sales_transactions()

    db.close()


if __name__ == "__main__":
    main()
