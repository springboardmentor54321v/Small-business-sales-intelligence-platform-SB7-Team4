import requests
import pandas as pd

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