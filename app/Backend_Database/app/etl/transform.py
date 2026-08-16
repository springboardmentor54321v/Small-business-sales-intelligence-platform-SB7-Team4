import pandas as pd
from pathlib import Path
import logging

# ===================================================
# Project Paths
# ===================================================

BASE_DIR = Path(__file__).parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

LOG_FILE = LOG_DIR / "etl.log"

# Create logs directory if it doesn't exist
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

INPUT_FILE = INPUT_DIR / "cleaned_dataset.csv"
OUTPUT_FILE = OUTPUT_DIR / "validated_dataset.csv"

# ===================================================
# Required Columns
# ===================================================

REQUIRED_COLUMNS = [
    "transaction_id",
    "invoice_id",
    "transaction_date",
    "customer_id",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "discount",
    "total_amount",
    "payment_method",
    "store_id",
    "created_by_user_id"
]

# ===================================================
# Dataset → Database Column Mapping
# ===================================================

COLUMN_MAPPING = {
    "Order ID": "invoice_id",
    "Order Date": "transaction_date",
    "Customer ID": "customer_id",
    "Product ID": "product_id",
    "Product Name": "product_name",
    "Category": "category",
    "Quantity": "quantity",
    "Discount": "discount",
    "Total amount": "total_amount",
    "unit_price": "unit_price"
}

# ===================================================
# Read Dataset
# ===================================================

try:
    print("\nStarting ETL Pipeline...")
    logger.info("ETL Pipeline Started")

    df = pd.read_csv(INPUT_FILE)

    logger.info(f"Dataset loaded successfully: {INPUT_FILE}")
    logger.info(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    print("=" * 60)
    print("ORIGINAL COLUMN NAMES")
    print("=" * 60)
    print(repr(df.columns.tolist()))

    # Rename columns
    df.rename(columns=COLUMN_MAPPING, inplace=True)

    print("\n" + "=" * 60)
    print("COLUMN NAMES AFTER MAPPING")
    print("=" * 60)
    print(repr(df.columns.tolist()))

    print("\n" + "=" * 60)
    print("MarketMind AI - ETL Pipeline")
    print("=" * 60)

    print(f"Dataset Loaded Successfully")
    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

except Exception as e:
    print(f"\nError reading dataset: {e}")
    exit()

# ===================================================
# Generate Unique Transaction IDs
# ===================================================

print("\nGenerating Unique Transaction IDs...")

df["transaction_id"] = [
    f"TXN{str(i).zfill(6)}"
    for i in range(1, len(df) + 1)
]

print("Unique Transaction IDs generated successfully.")

# ===================================================
# Display Column Names
# ===================================================

print("\nColumn Names")
print("-" * 60)

for column in df.columns:
    print(column)

# ===================================================
# Missing Values
# ===================================================

print("\nMissing Values")
print("-" * 60)

print(df.isnull().sum())

logger.info("Missing value analysis completed.")

# ===================================================
# Duplicate Rows
# ===================================================

print("\nDuplicate Rows")
print("-" * 60)

duplicate_rows = df.duplicated().sum()
print(duplicate_rows)
logger.info(f"Duplicate rows found: {duplicate_rows}")

# ===================================================
# Generate Payment Method
# ===================================================

print("\nGenerating Payment Method...")

# Payment information is not available in the dataset
df["payment_method"] = "Unknown"

print("Payment Method generated successfully.")

logger.info("Default payment_method assigned to all transactions.")

# ===================================================
# Generate Stores Table
# ===================================================

print("\nGenerating Stores Table...")

# Extract unique store locations
stores_df = (
    df[["City", "State", "Country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Generate store IDs
stores_df["store_id"] = range(1, len(stores_df) + 1)

# Generate store names
stores_df["store_name"] = (
    "Store_" +
    stores_df["City"].str.replace(" ", "_", regex=False)
)

# Generate location column
stores_df["location"] = (
    stores_df["City"] + ", " +
    stores_df["State"] + ", " +
    stores_df["Country"]
)

# Keep only required columns
stores_df = stores_df[
    [
        "store_id",
        "store_name",
        "location",
        "City",
        "State",
        "Country"
    ]
]

print(f"Total Stores Created : {len(stores_df)}")

# ===================================================
# Assign Store IDs to Sales Dataset
# ===================================================

df = df.merge(
    stores_df[
        [
            "store_id",
            "City",
            "State",
            "Country"
        ]
    ],
    on=["City", "State", "Country"],
    how="left"
)

print("Store IDs assigned successfully.")

# ===================================================
# Save Stores Table
# ===================================================

stores_output = OUTPUT_DIR / "stores.csv"

stores_df[
    [
        "store_id",
        "store_name",
        "location"
    ]
].to_csv(
    stores_output,
    index=False
)

logger.info(f"Stores table generated successfully. Total stores: {len(stores_df)}")

# ===================================================
# Generate created_by_user_id
# ===================================================

print("\nAssigning Default User...")

# Historical imported data is assigned to System Admin
df["created_by_user_id"] = 1

print("created_by_user_id assigned successfully.")
logger.info("created_by_user_id assigned to all transactions.")

# ===================================================
# Validate Required Columns
# ===================================================

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    print("\nDataset Validation Failed!")
    print("Missing Required Columns:")
    logger.error(f"Missing required columns: {missing_columns}")

    for column in missing_columns:
        print(f"- {column}")

else:
    print("\nAll required columns are present.")
    logger.info("Dataset validation completed successfully.")

# ===================================================
# Remove Invalid Rows
# ===================================================

available_required_columns = [
    col for col in REQUIRED_COLUMNS if col in df.columns
]

validated_df = df.dropna(subset=available_required_columns)

# ===================================================
# Validation Summary
# ===================================================

print("\nValidation Summary")
print("-" * 60)

print(f"Original Rows : {len(df)}")
print(f"Valid Rows    : {len(validated_df)}")
print(f"Removed Rows  : {len(df) - len(validated_df)}")

# ===================================================
# Save Dataset
# ===================================================

validated_df.to_csv(
    OUTPUT_FILE,
    index=False
)
logger.info(f"Validated dataset saved at: {OUTPUT_FILE}")

# ===================================================
# Generate Customers Table
# ===================================================

print("\nGenerating Customers Table...")

customers_df = (
    validated_df[
        [
            "customer_id",
            "Customer Name"
        ]
    ]
    .drop_duplicates(
        subset=["customer_id"],
        keep="first"
    )
    .reset_index(drop=True)
)

customers_df.rename(
    columns={
        "Customer Name": "name"
    },
    inplace=True
)

# Create placeholder email
customers_df["email"] = (
    customers_df["customer_id"].str.lower()
    + "@marketmind.ai"
)

# Placeholder phone
customers_df["phone"] = "Not Available"

customers_output = OUTPUT_DIR / "customers.csv"

customers_df.to_csv(
    customers_output,
    index=False
)

print(f"Customers Created : {len(customers_df)}")

logger.info(
    f"Customers table generated successfully. Total customers: {len(customers_df)}"
)

# ===================================================
# Generate Products Table
# ===================================================

print("\nGenerating Products Table...")

# Keep only one record for each product_id
# If a product appears multiple times with different prices,
# retain the last occurrence.
products_df = (
    validated_df[
        [
            "product_id",
            "product_name",
            "category",
            "unit_price"
        ]
    ]
    .drop_duplicates(
        subset=["product_id"],
        keep="last"
    )
    .reset_index(drop=True)
)

# Display summary
print(f"Unique Products : {len(products_df)}")

# Save products table
products_output = OUTPUT_DIR / "products.csv"

products_df.to_csv(
    products_output,
    index=False
)

logger.info(
    f"Products table generated successfully. Total unique products: {len(products_df)}"
)

# ===================================================
# Generate Inventory Table
# ===================================================

print("\nGenerating Inventory Table...")

inventory_df = (
    products_df[
        [
            "product_id"
        ]
    ]
    .copy()
)

# Generate simulated stock quantity
inventory_df["stock_quantity"] = 100

# Generate low stock threshold
inventory_df["low_stock_threshold"] = 20

inventory_output = OUTPUT_DIR / "inventory.csv"

inventory_df.to_csv(
    inventory_output,
    index=False
)

print(f"Inventory Records Created : {len(inventory_df)}")

logger.info(
    f"Inventory table generated successfully. Total records: {len(inventory_df)}"
)

# ===================================================
# Generate Sales Transactions Table
# ===================================================

print("\nGenerating Sales Transactions Table...")

sales_transactions_df = validated_df[
    [
        "transaction_id",
        "invoice_id",
        "transaction_date",
        "customer_id",
        "product_id",
        "store_id",
        "quantity",
        "unit_price",
        "discount",
        "total_amount",
        "payment_method",
        "created_by_user_id"
    ]
].copy()

sales_output = OUTPUT_DIR / "sales_transactions.csv"

sales_transactions_df.to_csv(
    sales_output,
    index=False
)

print(f"Sales Transactions Created : {len(sales_transactions_df)}")

logger.info(
    f"Sales Transactions table generated successfully. Total records: {len(sales_transactions_df)}"
)

print("\nETL Step Completed Successfully!")
logger.info("ETL Pipeline Completed Successfully.")
