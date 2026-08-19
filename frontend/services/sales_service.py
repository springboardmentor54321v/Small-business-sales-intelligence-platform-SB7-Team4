import streamlit as st
import pandas as pd
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.config import DB_BASE_URL


@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_sales(base_url=DB_BASE_URL):
    """
    Fetch all sales transactions from backend with concurrency and Streamlit caching.
    Returns the exact raw list of dictionaries without modifying any fields or values.
    """
    url_p1 = f"{base_url}/sales/?page=1&page_size=2000"
    first_page = None
    
    # 1. Fetch first page (handling possible Render cold-start)
    for attempt in range(3):
        try:
            timeout = 5 if attempt == 0 else 60
            r = requests.get(url_p1, timeout=timeout)
            r.raise_for_status()
            first_page = r.json()
            break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt == 2:
                return []
            time.sleep(2)
        except Exception:
            return []

    if not first_page or not isinstance(first_page, list):
        return []

    # If dataset fits in 1 page, return immediately
    if len(first_page) < 2000:
        return first_page

    # 2. Multi-page fetch using ThreadPoolExecutor for high throughput
    all_pages = {1: first_page}
    page = 2
    done = False

    def _fetch_single_page(p):
        try:
            res = requests.get(f"{base_url}/sales/?page={p}&page_size=2000", timeout=30)
            res.raise_for_status()
            data = res.json()
            return p, data if isinstance(data, list) else []
        except Exception:
            return p, []

    with ThreadPoolExecutor(max_workers=6) as executor:
        while not done:
            batch_pages = list(range(page, page + 6))
            futures = [executor.submit(_fetch_single_page, p) for p in batch_pages]
            for f in as_completed(futures):
                p, data = f.result()
                all_pages[p] = data

            for p in batch_pages:
                page_data = all_pages.get(p, [])
                if len(page_data) < 2000:
                    done = True
                    break
            page += 6

    # Assemble records strictly ordered by page
    ordered_sales = []
    for p in sorted(all_pages.keys()):
        ordered_sales.extend(all_pages[p])

    return ordered_sales


@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_sales_df(base_url=DB_BASE_URL):
    """
    Returns pre-processed sales DataFrame cached in memory to eliminate
    repetitive dataframe conversion and date parsing latency on reruns.
    """
    sales = fetch_all_sales(base_url)
    if not sales:
        return pd.DataFrame()

    df = pd.DataFrame(sales)

    numeric_sales = [
        "quantity",
        "unit_price",
        "discount",
        "total_amount"
    ]
    for col in numeric_sales:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"],
            errors="coerce"
        )
        df = df.sort_values(
            by="transaction_date",
            ascending=False
        )

    return df


@st.cache_data(ttl=600, show_spinner=False)
def fetch_inventory_data(base_url=DB_BASE_URL):
    """Fetch all inventory records from backend with caching."""
    url = f"{base_url}/inventory/"
    for attempt in range(3):
        try:
            timeout = 5 if attempt == 0 else 30
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, list) else []
        except Exception:
            if attempt == 2:
                return []
            time.sleep(1)
    return []


@st.cache_data(ttl=600, show_spinner=False)
def fetch_inventory_df(base_url=DB_BASE_URL):
    """Returns pre-processed inventory DataFrame cached in memory."""
    inv = fetch_inventory_data(base_url)
    if not inv:
        return pd.DataFrame()

    df = pd.DataFrame(inv)
    for col in ["stock_quantity", "low_stock_threshold"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


@st.cache_data(ttl=600, show_spinner=False)
def fetch_revenue_summary(base_url=DB_BASE_URL):
    """Fetch revenue summary dictionary from backend with caching."""
    url = f"{base_url}/revenue/summary"
    for attempt in range(3):
        try:
            timeout = 5 if attempt == 0 else 30
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            return data if isinstance(data, dict) else {}
        except Exception:
            if attempt == 2:
                return {}
            time.sleep(1)
    return {}


def clear_sales_cache():
    """Clear cached sales, inventory, and revenue data."""
    fetch_all_sales.clear()
    fetch_all_sales_df.clear()
    fetch_inventory_data.clear()
    fetch_inventory_df.clear()
    fetch_revenue_summary.clear()
