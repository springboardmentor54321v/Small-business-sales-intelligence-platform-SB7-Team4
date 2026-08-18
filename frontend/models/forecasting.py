import requests
import pandas as pd
import streamlit as st
import time

from config.config import AUTH_BASE_URL as BASE_URL


# ============================================================
# NORMAL FUTURE FORECAST
# ============================================================

def get_sales_forecast(uploaded_file):

    try:
        if isinstance(uploaded_file, pd.DataFrame):
            file_content = uploaded_file.to_csv(index=False).encode('utf-8')
            filename = "sales.csv"
        else:
            uploaded_file.seek(0)
            file_content = uploaded_file.read()
            uploaded_file.seek(0)
            filename = getattr(uploaded_file, "name", "sales.csv")

        files = {
            "file": (
                filename,
                file_content,
                "text/csv"
            )
        }

        response = None
        for attempt in range(4):
            try:
                timeout = 3 if attempt == 0 else 60
                if attempt > 0:
                    st.info(f"⏳ Connection attempt {attempt}/3 to the AI forecasting engine (Render is waking up)...")
                response = requests.post(
                    f"{BASE_URL}/predict",
                    files=files,
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
            raise requests.exceptions.RequestException("Failed to contact forecasting engine.")
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
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json().get("error", e.response.text)
            except Exception:
                error_detail = e.response.text
        elif 'response' in locals() and response is not None:
            try:
                error_detail = response.json().get("error", response.text)
            except Exception:
                error_detail = response.text
        return pd.DataFrame({
            "Error": [f"Forecast API Error: {error_detail}"]
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
        if isinstance(uploaded_file, pd.DataFrame):
            file_content = uploaded_file.to_csv(index=False).encode('utf-8')
            filename = "sales.csv"
        else:
            uploaded_file.seek(0)
            file_content = uploaded_file.read()
            uploaded_file.seek(0)
            filename = getattr(uploaded_file, "name", "sales.csv")

        files = {
            "file": (
                filename,
                file_content,
                "text/csv"
            )
        }

        response = None
        for attempt in range(4):
            try:
                timeout = 3 if attempt == 0 else 60
                if attempt > 0:
                    st.info(f"⏳ Connection attempt {attempt}/3 to the AI forecasting engine (Render is waking up)...")
                response = requests.post(
                    f"{BASE_URL}/forecast-backtest",
                    files=files,
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
            raise requests.exceptions.RequestException("Failed to contact forecasting engine.")
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
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json().get("error", e.response.text)
            except Exception:
                error_detail = e.response.text
        elif 'response' in locals() and response is not None:
            try:
                error_detail = response.json().get("error", response.text)
            except Exception:
                error_detail = response.text
        return {
            "results": pd.DataFrame(),
            "metrics": {},
            "period": {},
            "error": f"Forecast Backtest API Error: {error_detail}"
        }

    except Exception as e:
        return {
            "results": pd.DataFrame(),
            "metrics": {},
            "period": {},
            "error": str(e)
        }