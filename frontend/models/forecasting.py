import requests
import pandas as pd

from config.config import AUTH_BASE_URL as BASE_URL


# ============================================================
# NORMAL FUTURE FORECAST
# ============================================================

def get_sales_forecast(uploaded_file):

    try:

        uploaded_file.seek(0)
        file_content = uploaded_file.read()

        files = {
            "file": (
                uploaded_file.name,
                file_content,
                "text/csv"
            )
        }

        import streamlit as st
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                files=files,
                timeout=3
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            st.info("⏳ The AI Forecasting engine is currently waking up on Render. Performing analysis (up to 60 seconds)...")
            response = requests.post(
                f"{BASE_URL}/predict",
                files=files,
                timeout=60
            )

        if response.status_code in [502, 503]:
            st.info("⏳ Establishing connection to the AI forecasting engine (up to 60 seconds)...")
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
        file_content = uploaded_file.read()

        files = {
            "file": (
                uploaded_file.name,
                file_content,
                "text/csv"
            )
        }

        import streamlit as st
        try:
            response = requests.post(
                f"{BASE_URL}/forecast-backtest",
                files=files,
                timeout=3
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            st.info("⏳ The AI Forecasting engine is currently waking up on Render. Performing analysis (up to 60 seconds)...")
            response = requests.post(
                f"{BASE_URL}/forecast-backtest",
                files=files,
                timeout=60
            )

        if response.status_code in [502, 503]:
            st.info("⏳ Establishing connection to the AI forecasting engine (up to 60 seconds)...")
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