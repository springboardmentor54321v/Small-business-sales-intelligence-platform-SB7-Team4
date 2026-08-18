import os
import pandas as pd
import streamlit as st


def normalize_sales_df(df_input):
    """Normalize any uploaded sales DataFrame to ensure consistent columns across the app."""
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
        elif norm in ["product id", "product_id", "item_id", "product"]:
            col_map[col] = "product_id"
        elif norm in ["quantity", "qty", "units"]:
            col_map[col] = "quantity"
        elif norm in ["unit price", "unit_price", "price", "unitprice"]:
            col_map[col] = "unit_price"
        elif norm in ["category", "product_category"]:
            col_map[col] = "category"
        elif norm in ["product name", "product_name", "item_name"]:
            col_map[col] = "product_name"
        elif norm in ["payment method", "payment_method", "mode"]:
            col_map[col] = "payment_method"

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

    if "unit_price" not in df.columns:
        df["unit_price"] = df["total_amount"] / df["quantity"].replace(0, 1)

    if "category" not in df.columns:
        df["category"] = "General"

    if "payment_method" not in df.columns:
        df["payment_method"] = "Online"

    df = df.dropna(subset=["transaction_date"]).sort_values("transaction_date").reset_index(drop=True)
    return df


def get_default_sales_df():
    """Load default cleaned_dataset.csv (from AIML/week1/preprocessing) as primary dataset."""
    for path in [
        "AIML/week1/preprocessing/cleaned_dataset.csv",
        "../AIML/week1/preprocessing/cleaned_dataset.csv",
        "app/AIML/week1/preprocessing/cleaned_dataset.csv",
        "Backend_Database/app/etl/output/sales_transactions.csv",
        "../Backend_Database/app/etl/output/sales_transactions.csv",
        "app/Backend_Database/app/etl/output/sales_transactions.csv"
    ]:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                return normalize_sales_df(df)
            except Exception:
                pass
    return pd.DataFrame()


def get_default_inventory_df():
    """Load default inventory dataset."""
    for path in [
        "Backend_Database/app/etl/output/inventory.csv",
        "../Backend_Database/app/etl/output/inventory.csv",
        "app/Backend_Database/app/etl/output/inventory.csv"
    ]:
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except Exception:
                pass
    return pd.DataFrame()


def get_active_sales_df():
    """Retrieve currently active sales DataFrame (uploaded or default cleaned_dataset.csv)."""
    if "active_sales_df" in st.session_state and st.session_state["active_sales_df"] is not None:
        if not st.session_state["active_sales_df"].empty:
            return st.session_state["active_sales_df"]
    return get_default_sales_df()


def get_active_inventory_df():
    """Retrieve currently active inventory DataFrame."""
    if "active_inventory_df" in st.session_state and st.session_state["active_inventory_df"] is not None:
        if not st.session_state["active_inventory_df"].empty:
            return st.session_state["active_inventory_df"]
    return get_default_inventory_df()


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
