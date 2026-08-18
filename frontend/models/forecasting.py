import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import joblib

from config.config import AUTH_BASE_URL as BASE_URL

FORECAST_FEATURE_COLS = [
    "day", "month", "year", "dayofweek", "weekofyear", "quarter", "is_weekend",
    "lag1", "lag2", "lag3", "lag7", "lag14", "lag30",
    "log_lag1", "log_lag2", "log_lag3", "log_lag7", "log_lag14", "log_lag30",
    "rolling7", "rolling30", "log_rolling7", "log_rolling30",
    "ema7", "log_ema7"
]


def _build_forecast_row(history_df, future_date):
    """Exact feature constructor matching AIML/Integrated_API/app.py for Log-CatBoost."""
    amounts = history_df["Total amount"].values
    log_amounts = np.log1p(amounts)

    def get_lag(arr, lag):
        return float(arr[-lag]) if len(arr) >= lag else float(arr[0])

    def get_rolling(arr, window):
        sub = arr[-window:] if len(arr) >= window else arr
        return float(np.mean(sub))

    def get_ema(arr, span):
        return float(pd.Series(arr).ewm(span=span).mean().iloc[-1])

    row_dict = {
        "day": [future_date.day],
        "month": [future_date.month],
        "year": [future_date.year],
        "dayofweek": [future_date.dayofweek],
        "weekofyear": [int(future_date.isocalendar().week)],
        "quarter": [future_date.quarter],
        "is_weekend": [1 if future_date.dayofweek in [5, 6] else 0],
        "lag1": [get_lag(amounts, 1)],
        "lag2": [get_lag(amounts, 2)],
        "lag3": [get_lag(amounts, 3)],
        "lag7": [get_lag(amounts, 7)],
        "lag14": [get_lag(amounts, 14)],
        "lag30": [get_lag(amounts, 30)],
        "log_lag1": [get_lag(log_amounts, 1)],
        "log_lag2": [get_lag(log_amounts, 2)],
        "log_lag3": [get_lag(log_amounts, 3)],
        "log_lag7": [get_lag(log_amounts, 7)],
        "log_lag14": [get_lag(log_amounts, 14)],
        "log_lag30": [get_lag(log_amounts, 30)],
        "rolling7": [get_rolling(amounts, 7)],
        "rolling30": [get_rolling(amounts, 30)],
        "log_rolling7": [get_rolling(log_amounts, 7)],
        "log_rolling30": [get_rolling(log_amounts, 30)],
        "ema7": [get_ema(amounts, 7)],
        "log_ema7": [get_ema(log_amounts, 7)]
    }
    return pd.DataFrame(row_dict)[FORECAST_FEATURE_COLS]


def _run_local_catboost_backtest(uploaded_file):
    """Executes the exact trained Log-CatBoost backtest pipeline from AIML/Integrated_API/app.py."""
    try:
        model_path = "AIML/week3/forecasting/catboost/catboost_daily_model.pkl"
        if not os.path.exists(model_path):
            for alt in ["../" + model_path, "../../" + model_path]:
                if os.path.exists(alt):
                    model_path = alt
                    break

        if not os.path.exists(model_path):
            return None

        forecast_model = joblib.load(model_path)

        if isinstance(uploaded_file, pd.DataFrame):
            df = uploaded_file.copy()
        else:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)

        # Normalize column names cleanly
        col_map = {}
        for c in df.columns:
            norm = c.strip().lower()
            if norm in ["order date", "order_date", "date", "transaction_date", "orderdate"] or ("order" in norm and "date" in norm):
                col_map[c] = "Order Date"
            elif norm in ["total amount", "total_amount", "sales", "amount", "revenue", "totalsales"] or ("total" in norm and "amount" in norm):
                col_map[c] = "Total amount"
        df = df.rename(columns=col_map)

        if "Order Date" not in df.columns or "Total amount" not in df.columns:
            return None

        clean_df = pd.DataFrame({
            "Order Date": pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce"),
            "Total amount": pd.to_numeric(df["Total amount"], errors="coerce")
        }).dropna()

        daily_sales = (
            clean_df.groupby("Order Date")["Total amount"]
            .sum()
            .reset_index()
            .sort_values("Order Date")
            .reset_index(drop=True)
        )

        if len(daily_sales) < 35:
            return None

        test_size = 30
        train_data = daily_sales.iloc[:-test_size].copy()
        test_data = daily_sales.iloc[-test_size:].copy()
        history = train_data.copy()
        predictions = []

        for _, actual_row in test_data.iterrows():
            prediction_date = actual_row["Order Date"]
            row = _build_forecast_row(history, prediction_date)

            pred_log = float(forecast_model.predict(row)[0])
            pred_val = max(0.0, float(np.expm1(pred_log)))

            predictions.append({
                "Order Date": prediction_date.strftime("%Y-%m-%d"),
                "Actual Sales": round(float(actual_row["Total amount"]), 2),
                "Predicted Sales": round(pred_val, 2),
            })
            history.loc[len(history)] = [prediction_date, float(actual_row["Total amount"])]

        actual_values = np.array([item["Actual Sales"] for item in predictions])
        predicted_values = np.array([item["Predicted Sales"] for item in predictions])

        mae = float(np.mean(np.abs(actual_values - predicted_values)))
        rmse = float(np.sqrt(np.mean((actual_values - predicted_values) ** 2)))
        sum_actual = float(np.sum(actual_values))
        wape = float(np.sum(np.abs(actual_values - predicted_values)) / max(sum_actual, 1.0) * 100)
        pct_errs = [abs((a - p) / a) * 100 for a, p in zip(actual_values, predicted_values) if a > 0]
        mape = float(np.mean(pct_errs)) if pct_errs else 0.0

        return {
            "results": pd.DataFrame(predictions),
            "metrics": {
                "MAE": round(mae, 2),
                "RMSE": round(rmse, 2),
                "WAPE": round(wape, 2),
                "MAPE": round(mape, 2),
                "Days Evaluated": len(predictions)
            },
            "period": {
                "Start": test_data["Order Date"].min().strftime("%Y-%m-%d"),
                "End": test_data["Order Date"].max().strftime("%Y-%m-%d")
            },
            "error": None
        }
    except Exception as e:
        return None


def _run_local_catboost_forecast(uploaded_file, periods=30):
    """Executes the exact trained Log-CatBoost 30-day forecast pipeline from AIML/Integrated_API/app.py."""
    try:
        model_path = "AIML/week3/forecasting/catboost/catboost_daily_model.pkl"
        if not os.path.exists(model_path):
            for alt in ["../" + model_path, "../../" + model_path]:
                if os.path.exists(alt):
                    model_path = alt
                    break

        if not os.path.exists(model_path):
            return None

        forecast_model = joblib.load(model_path)

        if isinstance(uploaded_file, pd.DataFrame):
            df = uploaded_file.copy()
        else:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)

        col_map = {}
        for c in df.columns:
            norm = c.strip().lower()
            if norm in ["order date", "order_date", "date", "transaction_date", "orderdate"] or ("order" in norm and "date" in norm):
                col_map[c] = "Order Date"
            elif norm in ["total amount", "total_amount", "sales", "amount", "revenue", "totalsales"] or ("total" in norm and "amount" in norm):
                col_map[c] = "Total amount"
        df = df.rename(columns=col_map)

        if "Order Date" not in df.columns or "Total amount" not in df.columns:
            return None

        clean_df = pd.DataFrame({
            "Order Date": pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce"),
            "Total amount": pd.to_numeric(df["Total amount"], errors="coerce")
        }).dropna()

        daily_sales = clean_df.groupby("Order Date")["Total amount"].sum().reset_index().sort_values("Order Date").reset_index(drop=True)
        if daily_sales.empty:
            return None

        history = daily_sales.copy()
        predictions = []

        for _ in range(periods):
            future_date = history["Order Date"].iloc[-1] + pd.Timedelta(days=1)
            row = _build_forecast_row(history, future_date)

            pred_log = float(forecast_model.predict(row)[0])
            pred_val = max(0.0, float(np.expm1(pred_log)))

            spread = pred_val * 0.22 + 150.0
            lower_bound = max(0.0, round(pred_val - 1.96 * spread, 2))
            upper_bound = round(pred_val + 1.96 * spread, 2)

            recent_sales = history["Total amount"].tail(30)
            recent_mean = float(recent_sales.mean())
            recent_std = float(recent_sales.std()) if len(recent_sales) > 1 and recent_sales.std() > 0 else (recent_mean * 0.2)

            difference = abs(pred_val - recent_mean)
            confidence = "High" if difference <= recent_std else ("Medium" if difference <= 2.0 * recent_std else "Low")

            predictions.append({
                "Order Date": future_date.strftime("%Y-%m-%d"),
                "Predicted Sales": round(pred_val, 2),
                "Lower Bound (95% CI)": lower_bound,
                "Upper Bound (95% CI)": upper_bound,
                "Confidence": confidence
            })
            history.loc[len(history)] = [future_date, pred_val]

        return pd.DataFrame(predictions)
    except Exception:
        return None


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

        # 1. Try remote backend API
        response = None
        for attempt in range(2):
            try:
                response = requests.post(
                    f"{BASE_URL}/predict",
                    files=files,
                    timeout=3
                )
                if response.status_code == 200:
                    break
            except Exception:
                pass

        if response is not None and response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return pd.DataFrame(data)
            if isinstance(data, dict) and "error" not in data:
                return pd.DataFrame([data])
    except Exception:
        pass

    # 2. Local CatBoost Pipeline (Identical to backend API)
    local_df = _run_local_catboost_forecast(uploaded_file)
    if local_df is not None and not local_df.empty:
        return local_df

    return pd.DataFrame({
        "Error": ["Unable to generate sales forecast. Please verify your CSV format."]
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

        # 1. Try remote backend API
        response = None
        for attempt in range(2):
            try:
                response = requests.post(
                    f"{BASE_URL}/forecast-backtest",
                    files=files,
                    timeout=3
                )
                if response.status_code == 200:
                    break
            except Exception:
                pass

        if response is not None and response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "Results" in data:
                return {
                    "results": pd.DataFrame(data.get("Results", [])),
                    "metrics": data.get("Evaluation Metrics", {}),
                    "period": data.get("Backtest Period", {}),
                    "error": None
                }
    except Exception:
        pass

    # 2. Local CatBoost Pipeline (Identical to backend API)
    local_res = _run_local_catboost_backtest(uploaded_file)
    if local_res is not None:
        return local_res

    return {
        "results": pd.DataFrame(),
        "metrics": {},
        "period": {},
        "error": "Unable to complete forecast backtest. Please check your CSV format."
    }