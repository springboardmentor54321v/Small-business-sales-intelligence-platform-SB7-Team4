import requests
import pandas as pd
import streamlit as st

from config.config import AUTH_BASE_URL as BASE_URL


def get_anomaly_alerts(order_date="2011-01-04"):

    try:

        payload = {
            "Order Date": order_date.strip()
        }

        import time
        response = None
        status_box = st.empty()
        for attempt in range(4):
            try:
                if attempt > 0:
                    status_box.info(f"⏳ Connecting to AI Anomaly engine (attempt {attempt}/3)...")
                response = requests.post(
                    f"{BASE_URL}/check-anomaly",
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
            raise requests.exceptions.RequestException("Failed to contact Anomaly engine.")
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