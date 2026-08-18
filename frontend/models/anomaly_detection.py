import requests
import pandas as pd

from config.config import AUTH_BASE_URL as BASE_URL


def get_anomaly_alerts(order_date="2011-01-04"):

    try:

        payload = {
            "Order Date": order_date.strip()
        }

        import streamlit as st
        try:
            response = requests.post(
                f"{BASE_URL}/check-anomaly",
                json=payload,
                timeout=3
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            st.info("⏳ The AI Anomaly engine is currently waking up on Render. Performing analysis (up to 60 seconds)...")
            response = requests.post(
                f"{BASE_URL}/check-anomaly",
                json=payload,
                timeout=60
            )

        if response.status_code in [502, 503]:
            st.info("⏳ Establishing connection to the AI anomaly engine (up to 60 seconds)...")
            response = requests.post(
                f"{BASE_URL}/check-anomaly",
                json=payload,
                timeout=60
            )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return pd.DataFrame(data)

        if isinstance(data, dict):
            return pd.DataFrame([data])

        return pd.DataFrame({
            "Message": ["No anomaly data found."]
        })

    except requests.exceptions.HTTPError:

        try:
            error = response.json().get("error", response.text)
        except Exception:
            error = response.text

        return pd.DataFrame({
            "Error": [error]
        })

    except requests.exceptions.RequestException as e:

        return pd.DataFrame({
            "Error": [f"API Connection Error: {e}"]
        })

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })