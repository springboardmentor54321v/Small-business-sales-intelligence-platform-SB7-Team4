import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"


def get_churn_risk(customer_id="AA-10315"):

    try:

        payload = {
            "Customer ID": customer_id
        }

        response = requests.post(
            f"{BASE_URL}/churn-risk",
            json=payload,
            timeout=10
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