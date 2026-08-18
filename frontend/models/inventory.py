import requests
import pandas as pd
import streamlit as st
from config.config import DB_BASE_URL as BASE_URL
from models.data_loader import get_active_inventory_df


def get_inventory():
    # 1. Primary: Use active dataset inventory
    inv_df = get_active_inventory_df()
    if inv_df is not None and not inv_df.empty:
        return inv_df

    # 2. Remote API fallback
    try:
        response = requests.get(f"{BASE_URL}/inventory/", timeout=3.5)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if not df.empty:
                df["stock_quantity"] = pd.to_numeric(df.get("stock_quantity", 0), errors="coerce").fillna(0)
                df["low_stock_threshold"] = pd.to_numeric(df.get("low_stock_threshold", 20), errors="coerce").fillna(20)
                df["Status"] = df.apply(
                    lambda row: "Low Stock" if row["stock_quantity"] <= row["low_stock_threshold"] else "In Stock",
                    axis=1
                )
                return df
    except Exception:
        pass

    return get_active_inventory_df()