import requests
import pandas as pd

from config.config import AUTH_BASE_URL as BASE_URL


def get_anomaly_alerts(order_date="2011-01-04"):

    try:

        payload = {
            "Order Date": order_date.strip()
        }

        response = requests.post(
            f"{BASE_URL}/check-anomaly",
            json=payload,
            timeout=10
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