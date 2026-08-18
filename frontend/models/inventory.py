import requests
import pandas as pd
import streamlit as st
from config.config import DB_BASE_URL as BASE_URL


@st.cache_data(ttl=180, show_spinner=False)
def get_inventory():

    try:

        response = requests.get(
            f"{BASE_URL}/inventory/",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data)

        if df.empty:
            return pd.DataFrame({
                "Message": ["No inventory data found."]
            })

        expected_columns = [
            "id",
            "product_id",
            "stock_quantity",
            "low_stock_threshold"
        ]

        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        df["stock_quantity"] = pd.to_numeric(
            df["stock_quantity"],
            errors="coerce"
        ).fillna(0)

        df["low_stock_threshold"] = pd.to_numeric(
            df["low_stock_threshold"],
            errors="coerce"
        ).fillna(0)

        df["Status"] = df.apply(
            lambda row: "Low Stock"
            if row["stock_quantity"] <= row["low_stock_threshold"]
            else "In Stock",
            axis=1
        )

        return df

    except requests.exceptions.Timeout:

        return pd.DataFrame({
            "Error": ["Backend request timed out."]
        })

    except requests.exceptions.ConnectionError:

        return pd.DataFrame({
            "Error": ["Unable to connect to backend."]
        })

    except requests.exceptions.HTTPError as e:

        return pd.DataFrame({
            "Error": [f"HTTP Error: {e}"]
        })

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })