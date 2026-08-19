import requests
import pandas as pd
import streamlit as st

from config.config import AUTH_BASE_URL as BASE_URL


def get_churn_risk(customer_id="AA-10315"):

    try:

        payload = {
            "Customer ID": customer_id
        }

        import time
        response = None
        for attempt in range(4):
            try:
                timeout = 3 if attempt == 0 else 60
                if attempt > 0:
                    st.info(f"⏳ Connection attempt {attempt}/3 to the AI Churn engine (Render is waking up)...")
                response = requests.post(
                    f"{BASE_URL}/churn-risk",
                    json=payload,
                    timeout=timeout
                )
                if response.status_code not in [502, 503]:
                    break
                time.sleep(3)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt == 3:
                    raise
                time.sleep(3)

        if response is None:
            raise requests.exceptions.RequestException("Failed to contact Churn engine.")
        
        if response.status_code == 404:
            try:
                res_data = response.json()
                error_msg = res_data.get("error", res_data.get("detail", f"Customer ID '{customer_id}' not found."))
            except Exception:
                error_msg = f"Customer ID '{customer_id}' was not found in the database."
            return pd.DataFrame({"Error": [error_msg]})

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            if "error" in data:
                return pd.DataFrame({"Error": [data["error"]]})
            return pd.DataFrame([data])

        if isinstance(data, list):
            return pd.DataFrame(data)

        return pd.DataFrame({
            "Message": ["No churn prediction found."]
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