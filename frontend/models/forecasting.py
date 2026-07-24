import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"


def get_sales_forecast(uploaded_file):

    try:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "text/csv"
            )
        }

        response = requests.post(
            f"{BASE_URL}/predict",
            files=files,
            timeout=60
        )

        # ---------- DEBUG ----------
        print("\n" + "=" * 60)
        print("FORECAST API DEBUG")
        print("=" * 60)
        print("Status Code:", response.status_code)
        print("Response Body:")
        print(response.text)
        print("=" * 60 + "\n")
        # ---------------------------

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            df = pd.DataFrame(data)
            print("Forecast DataFrame Columns:", df.columns.tolist())
            return df

        if isinstance(data, dict):
            df = pd.DataFrame([data])
            print("Forecast DataFrame Columns:", df.columns.tolist())
            return df

        return pd.DataFrame({
            "Error": ["No forecast data returned from API."]
        })

    except requests.exceptions.RequestException as e:

        print("\nREQUEST EXCEPTION")
        print(e)

        if 'response' in locals():
            print("Status Code:", response.status_code)
            print("Response Body:")
            print(response.text)

        return pd.DataFrame({
            "Error": [str(e)]
        })

    except Exception as e:

        print("\nUNEXPECTED ERROR")
        print(str(e))

        return pd.DataFrame({
            "Error": [str(e)]
        })