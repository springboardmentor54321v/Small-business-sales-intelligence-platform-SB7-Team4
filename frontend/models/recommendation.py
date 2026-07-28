import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"


def get_recommendations(product_name="Staples"):

    try:

        payload = {
            "Product Name": product_name
        }

        response = requests.post(
            f"{BASE_URL}/recommend-product",
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # If API returns a list
        if isinstance(data, list):
            return pd.DataFrame(data)

        # If API returns a dictionary
        elif isinstance(data, dict):

            if "Recommended Products" in data:

                return pd.DataFrame({
                    "Recommended Products": data["Recommended Products"]
                })

            return pd.DataFrame([data])

        # Unknown response
        return pd.DataFrame({
            "Message": ["No recommendations found."]
        })

    except requests.exceptions.RequestException as e:

        return pd.DataFrame({
            "Error": [f"API Connection Error: {e}"]
        })

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })