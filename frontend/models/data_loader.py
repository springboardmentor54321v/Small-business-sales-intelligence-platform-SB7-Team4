import os
import hashlib
import pandas as pd
import streamlit as st


def normalize_sales_df(df_input):
    """Normalize any sales DataFrame to ensure consistent columns across the application."""
    if df_input is None or df_input.empty:
        return pd.DataFrame()

    df = df_input.copy()
    col_map = {}
    for col in df.columns:
        norm = str(col).strip().lower()
        if norm in ["order date", "order_date", "date", "transaction_date"]:
            col_map[col] = "transaction_date"
        elif norm in ["total amount", "total_amount", "sales", "amount", "revenue", "totalsales", "total_sales"]:
            col_map[col] = "total_amount"
        elif norm in ["customer id", "customer_id", "cust_id", "customer"]:
            col_map[col] = "customer_id"
        elif norm in ["customer name", "customer_name", "cust_name"]:
            col_map[col] = "customer_name"
        elif norm in ["product id", "product_id", "item_id", "product"]:
            col_map[col] = "product_id"
        elif norm in ["product name", "product_name", "item_name"]:
            col_map[col] = "product_name"
        elif norm in ["quantity", "qty", "units"]:
            col_map[col] = "quantity"
        elif norm in ["unit price", "unit_price", "price", "unitprice"]:
            col_map[col] = "unit_price"
        elif norm in ["category", "product_category"]:
            col_map[col] = "category"
        elif norm in ["sub-category", "sub_category", "subcategory"]:
            col_map[col] = "sub_category"
        elif norm in ["payment method", "payment_method", "mode"]:
            col_map[col] = "payment_method"
        elif norm in ["invoice id", "invoice_id", "order id", "order_id"]:
            col_map[col] = "invoice_id"
        elif norm in ["transaction id", "transaction_id", "row id", "row_id"]:
            col_map[col] = "transaction_id"

    df = df.rename(columns=col_map)

    # 1. Date conversion
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True, errors="coerce")
    else:
        df["transaction_date"] = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq="D")

    # 2. Total Amount conversion
    if "total_amount" in df.columns:
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0.0)
    else:
        df["total_amount"] = 100.0

    # 3. Fill missing optional columns with intelligent defaults
    if "quantity" not in df.columns:
        df["quantity"] = 1
    else:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)

    if "product_id" not in df.columns:
        df["product_id"] = "PROD-GENERIC"

    if "product_name" not in df.columns:
        df["product_name"] = df["product_id"]

    if "customer_id" not in df.columns:
        df["customer_id"] = "CUST-GENERIC"

    if "customer_name" not in df.columns:
        df["customer_name"] = df["customer_id"]

    if "unit_price" not in df.columns:
        df["unit_price"] = (df["total_amount"] / df["quantity"].replace(0, 1)).round(2)

    if "category" not in df.columns:
        df["category"] = "General"

    if "invoice_id" not in df.columns:
        df["invoice_id"] = [f"INV-{i+10001}" for i in range(len(df))]

    if "transaction_id" not in df.columns:
        df["transaction_id"] = [f"TXN-{i+10001}" for i in range(len(df))]

    if "payment_method" not in df.columns:
        df["payment_method"] = "Online"

    df = df.dropna(subset=["transaction_date"]).sort_values("transaction_date").reset_index(drop=True)
    return df


def get_default_sales_df():
    """Load default cleaned_dataset.csv (from AIML/week1/preprocessing) as primary baseline dataset."""
    for path in [
        "AIML/week1/preprocessing/cleaned_dataset.csv",
        "../AIML/week1/preprocessing/cleaned_dataset.csv",
        "app/AIML/week1/preprocessing/cleaned_dataset.csv",
        "Backend_Database/app/etl/output/sales_transactions.csv",
        "../Backend_Database/app/etl/output/sales_transactions.csv"
    ]:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                return normalize_sales_df(df)
            except Exception:
                pass
    return pd.DataFrame()


def build_inventory_from_sales(sales_df):
    """Generate dynamic, realistic inventory catalog matching the products in the active dataset."""
    if sales_df is None or sales_df.empty:
        return pd.DataFrame()

    prod_col = "product_id"
    name_col = "product_name" if "product_name" in sales_df.columns else prod_col
    cat_col = "category" if "category" in sales_df.columns else None
    price_col = "unit_price" if "unit_price" in sales_df.columns else "total_amount"

    unique_prods = sales_df[[prod_col]].drop_duplicates().copy()
    if name_col in sales_df.columns:
        unique_prods["product_name"] = sales_df.groupby(prod_col)[name_col].first().values
    else:
        unique_prods["product_name"] = unique_prods[prod_col]

    if cat_col and cat_col in sales_df.columns:
        unique_prods["category"] = sales_df.groupby(prod_col)[cat_col].first().values
    else:
        unique_prods["category"] = "General"

    if price_col in sales_df.columns:
        unique_prods["unit_price"] = sales_df.groupby(prod_col)[price_col].mean().round(2).values
    else:
        unique_prods["unit_price"] = 25.0

    stocks = []
    thresholds = []
    statuses = []

    for pid in unique_prods[prod_col]:
        h = int(hashlib.md5(str(pid).encode("utf-8")).hexdigest(), 16)
        # Produce ~1.5% low stock items (~25 out of 1862) with realistic stock numbers
        if (h % 100) < 2:
            stock = 3 + (h % 16) # stock between 3 and 18 (<= 20)
        else:
            stock = 35 + (h % 90) # healthy stock between 35 and 124
        thresh = 20
        status = "Low Stock" if stock <= thresh else "In Stock"
        stocks.append(stock)
        thresholds.append(thresh)
        statuses.append(status)

    unique_prods["stock_quantity"] = stocks
    unique_prods["low_stock_threshold"] = thresholds
    unique_prods["Status"] = statuses
    unique_prods["id"] = range(1, len(unique_prods) + 1)
    return unique_prods.reset_index(drop=True)


def get_active_sales_df():
    """Retrieve currently active sales DataFrame (uploaded or default cleaned_dataset.csv)."""
    if "active_sales_df" in st.session_state and st.session_state["active_sales_df"] is not None:
        if not st.session_state["active_sales_df"].empty:
            return st.session_state["active_sales_df"]
    return get_default_sales_df()


def get_active_inventory_df():
    """Retrieve currently active inventory DataFrame matching the active dataset."""
    sales_df = get_active_sales_df()
    return build_inventory_from_sales(sales_df)


def set_active_sales_df(df_input, dataset_name="Custom Upload"):
    """Set uploaded dataset as the active dataset across the entire application."""
    normalized_df = normalize_sales_df(df_input)
    st.session_state["active_sales_df"] = normalized_df
    st.session_state["active_dataset_name"] = dataset_name
    st.cache_data.clear()
    return normalized_df


def reset_to_default_dataset():
    """Reset application data back to default cleaned_dataset.csv."""
    st.session_state["active_sales_df"] = None
    st.session_state["active_dataset_name"] = "Cleaned Retail Dataset (Primary)"
    st.cache_data.clear()
