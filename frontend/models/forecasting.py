import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"


# ============================================================
# NORMAL FUTURE FORECAST
# ============================================================

def get_sales_forecast(uploaded_file):

    try:

        uploaded_file.seek(0)

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

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):

            return pd.DataFrame(data)

        if isinstance(data, dict):

            if "error" in data:

                return pd.DataFrame({
                    "Error": [data["error"]]
                })

            return pd.DataFrame([data])

        return pd.DataFrame()

    except requests.exceptions.RequestException as e:

        return pd.DataFrame({
            "Error": [f"Forecast API Error: {e}"]
        })

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })


# ============================================================
# FORECAST VS ACTUAL BACKTEST
# ============================================================

def get_forecast_backtest(uploaded_file):

    try:

        uploaded_file.seek(0)

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "text/csv"
            )
        }

        response = requests.post(
            f"{BASE_URL}/forecast-backtest",
            files=files,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        # --------------------------------------------
        # API ERROR
        # --------------------------------------------

        if isinstance(data, dict) and "error" in data:

            return {
                "results": pd.DataFrame(),
                "metrics": {},
                "period": {},
                "error": data["error"]
            }

        # --------------------------------------------
        # RESULTS
        # --------------------------------------------

        results = data.get(
            "Results",
            []
        )

        results_df = pd.DataFrame(results)

        # --------------------------------------------
        # METRICS
        # --------------------------------------------

        metrics = data.get(
            "Evaluation Metrics",
            {}
        )

        # --------------------------------------------
        # BACKTEST PERIOD
        # --------------------------------------------

        period = data.get(
            "Backtest Period",
            {}
        )

        return {
            "results": results_df,
            "metrics": metrics,
            "period": period,
            "error": None
        }

    except requests.exceptions.Timeout:

        return {
            "results": pd.DataFrame(),
            "metrics": {},
            "period": {},
            "error": "Forecast backtest API timed out."
        }

    except requests.exceptions.ConnectionError:

        return {
            "results": pd.DataFrame(),
            "metrics": {},
            "period": {},
            "error": "Unable to connect to Forecast Backtest API."
        }

    except requests.exceptions.HTTPError as e:

        return {
            "results": pd.DataFrame(),
            "metrics": {},
            "period": {},
            "error": f"Forecast Backtest API Error: {e}"
        }

    except Exception as e:

        return {
            "results": pd.DataFrame(),
            "metrics": {},
            "period": {},
            "error": str(e)
        }