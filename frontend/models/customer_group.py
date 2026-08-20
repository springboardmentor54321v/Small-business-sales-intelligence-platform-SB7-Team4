import requests
import pandas as pd
import streamlit as st
import time

from config.config import AUTH_BASE_URL as BASE_URL


def get_customer_group(customer_id="AA-10315"):

    try:
        payload = {
            "Customer ID": customer_id.strip()
        }

        response = None
        status_box = st.empty()
        for attempt in range(4):
            try:
                if attempt > 0:
                    status_box.info(f"⏳ Connecting to Customer Grouping engine (attempt {attempt}/3)...")
                response = requests.post(
                    f"{BASE_URL}/customer-group",
                    json=payload,
                    timeout=45
                )
                if response.status_code not in [502, 503]:
                    break
                time.sleep(2)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt == 3:
                    raise
                time.sleep(2)

        status_box.empty()

        if response is None:
            raise requests.exceptions.RequestException("Failed to contact Customer Grouping engine.")

        if response.status_code == 404:
            return pd.DataFrame([{
                "Customer ID": customer_id,
                "Customer Segment": "New / Cold-Start Customer",
                "Cluster": "Baseline Group",
                "Total Orders": 1,
                "Total Revenue": "₹0.00",
                "Recency (Days)": 0,
                "Profile Status": f"Baseline Profile (Customer ID '{customer_id}')"
            }])

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            if "error" in data:
                return pd.DataFrame({"Error": [data["error"]]})

            if data.get("is_cold_start") or (data.get("Total Orders", 0) == 0 and data.get("Total Revenue", 0) == 0):
                return pd.DataFrame([{
                    "Customer ID": customer_id,
                    "Customer Segment": "New / Cold-Start Customer",
                    "Cluster": "Baseline Group",
                    "Total Orders": data.get("Total Orders", 1),
                    "Total Revenue": f"₹{data.get('Total Revenue', 0):,.2f}",
                    "Recency (Days)": data.get("Recency", 0),
                    "Profile Status": f"Baseline Profile (Customer ID '{customer_id}')"
                }])

            return pd.DataFrame([data])

        if isinstance(data, list):
            return pd.DataFrame(data)

        return pd.DataFrame({
            "Message": ["No customer group found."]
        })

    except requests.exceptions.HTTPError as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                res_data = e.response.json()
                error_detail = res_data.get("error", res_data.get("detail", e.response.text))
            except Exception:
                error_detail = e.response.text
        return pd.DataFrame({
            "Error": [error_detail]
        })

    except requests.exceptions.RequestException as e:
        return pd.DataFrame({
            "Error": [f"API Connection Error: {e}"]
        })

    except Exception as e:
        return pd.DataFrame({
            "Error": [str(e)]
        })