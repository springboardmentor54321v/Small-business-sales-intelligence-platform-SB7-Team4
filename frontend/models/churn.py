import requests
import pandas as pd

from config.config import AUTH_BASE_URL as BASE_URL


def get_churn_risk(customer_id="AA-10315"):

    try:

        payload = {
            "Customer ID": customer_id
        }

        import streamlit as st
        try:
            response = requests.post(
                f"{BASE_URL}/churn-risk",
                json=payload,
                timeout=3
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            st.info("⏳ The AI Churn prediction engine is currently waking up on Render. Performing analysis (up to 35 seconds)...")
            response = requests.post(
                f"{BASE_URL}/churn-risk",
                json=payload,
                timeout=35
            )

        if response.status_code in [502, 503]:
            st.info("⏳ Establishing connection to the AI prediction engine (up to 35 seconds)...")
            response = requests.post(
                f"{BASE_URL}/churn-risk",
                json=payload,
                timeout=35
            )

        response.raise_for_status()

        data = response.json()

        print("\n" + "=" * 60)
        print("CHURN API RESPONSE")
        print("=" * 60)
        print(data)
        print("=" * 60)

        if isinstance(data, dict):
            return pd.DataFrame([data])

        if isinstance(data, list):
            return pd.DataFrame(data)

        return pd.DataFrame({
            "Message": ["No churn prediction found."]
        })

    except requests.exceptions.RequestException as e:

        return pd.DataFrame({
            "Error": [f"API Connection Error: {e}"]
        })

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })