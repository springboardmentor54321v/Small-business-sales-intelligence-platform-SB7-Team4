import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import joblib

from config.config import AUTH_BASE_URL as BASE_URL


# ============================================================
# TRAINED LOCAL ML MODEL FALLBACKS
# ============================================================

def _local_backtest_from_csv(uploaded_file):
    """Executes historical backtest using trained Random Forest Regressor when remote API drops connection."""
    try:
        model_path = "AIML/week3/forecasting/random_forest/random_forest_daily_model.pkl"
        if not os.path.exists(model_path):
            for alt in ["../" + model_path, "../../" + model_path]:
                if os.path.exists(alt):
                    model_path = alt
                    break

        if not os.path.exists(model_path):
            return None

        rf_model = joblib.load(model_path)

        if isinstance(uploaded_file, pd.DataFrame):
            df = uploaded_file.copy()
        else:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)

        # Precise Column Mapping to prevent duplicate column names
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

        # Keep only the target columns to prevent any duplicate column collisions
        sub_df = pd.DataFrame({
            "Order Date": pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce"),
            "Total amount": pd.to_numeric(df["Total amount"], errors="coerce")
        }).dropna()

        daily_sales = (
            sub_df.groupby("Order Date")["Total amount"]
            .sum()
            .reset_index()
            .sort_values("Order Date")
            .reset_index(drop=True)
        )

        if len(daily_sales) < 35:
            return None

        test_size = min(30, len(daily_sales) // 4)
        train_data = daily_sales.iloc[:-test_size].copy()
        test_data = daily_sales.iloc[-test_size:].copy()

        history = train_data.copy()
        results = []

        for _, row in test_data.iterrows():
            pred_date = row["Order Date"]
            last30 = history["Total amount"].values[-30:] if len(history) >= 30 else history["Total amount"].values
            last7 = history["Total amount"].values[-7:] if len(history) >= 7 else history["Total amount"].values

            feat = pd.DataFrame([{
                "day": pred_date.day,
                "month": pred_date.month,
                "year": pred_date.year,
                "dayofweek": pred_date.dayofweek,
                "weekofyear": int(pred_date.isocalendar().week),
                "quarter": pred_date.quarter,
                "lag1": float(history["Total amount"].iloc[-1]),
                "lag7": float(history["Total amount"].iloc[-7]) if len(history) >= 7 else float(history["Total amount"].iloc[-1]),
                "lag30": float(history["Total amount"].iloc[-30]) if len(history) >= 30 else float(history["Total amount"].iloc[-1]),
                "rolling7": float(np.mean(last7)),
                "rolling30": float(np.mean(last30))
            }])

            pred_val = float(rf_model.predict(feat)[0])
            results.append({
                "Order Date": pred_date.strftime("%Y-%m-%d"),
                "Actual Sales": round(float(row["Total amount"]), 2),
                "Predicted Sales": round(max(0.0, pred_val), 2)
            })
            history.loc[len(history)] = [pred_date, row["Total amount"]]

        res_df = pd.DataFrame(results)
        actuals = res_df["Actual Sales"].values
        preds = res_df["Predicted Sales"].values

        mae = float(np.mean(np.abs(actuals - preds)))
        rmse = float(np.sqrt(np.mean((actuals - preds) ** 2)))
        wape = float(np.sum(np.abs(actuals - preds)) / max(1e-6, np.sum(actuals)) * 100)
        accuracy = max(0.0, 100.0 - wape)

        return {
            "results": res_df,
            "metrics": {
                "MAE": round(mae, 2),
                "RMSE": round(rmse, 2),
                "WAPE": f"{round(wape, 2)}%",
                "Accuracy": f"{round(accuracy, 2)}%",
                "Evaluated Days": len(res_df)
            },
            "period": {
                "Start Date": res_df["Order Date"].min(),
                "End Date": res_df["Order Date"].max()
            },
            "error": None
        }
    except Exception:
        return None


def _local_forecast_from_csv(uploaded_file, periods=30):
    """Executes future sales forecasting using trained Random Forest Regressor."""
    try:
        model_path = "AIML/week3/forecasting/random_forest/random_forest_daily_model.pkl"
        if not os.path.exists(model_path):
            for alt in ["../" + model_path, "../../" + model_path]:
                if os.path.exists(alt):
                    model_path = alt
                    break

        if not os.path.exists(model_path):
            return None

        rf_model = joblib.load(model_path)

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

        sub_df = pd.DataFrame({
            "Order Date": pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce"),
            "Total amount": pd.to_numeric(df["Total amount"], errors="coerce")
        }).dropna()

        daily = sub_df.groupby("Order Date")["Total amount"].sum().reset_index().sort_values("Order Date").reset_index(drop=True)
        if daily.empty:
            return None

        history = daily.copy()
        last_date = daily["Order Date"].max()
        preds = []

        for step in range(1, periods + 1):
            future_date = last_date + pd.Timedelta(days=step)
            last30 = history["Total amount"].values[-30:] if len(history) >= 30 else history["Total amount"].values
            last7 = history["Total amount"].values[-7:] if len(history) >= 7 else history["Total amount"].values

            feat = pd.DataFrame([{
                "day": future_date.day,
                "month": future_date.month,
                "year": future_date.year,
                "dayofweek": future_date.dayofweek,
                "weekofyear": int(future_date.isocalendar().week),
                "quarter": future_date.quarter,
                "lag1": float(history["Total amount"].iloc[-1]),
                "lag7": float(history["Total amount"].iloc[-7]) if len(history) >= 7 else float(history["Total amount"].iloc[-1]),
                "lag30": float(history["Total amount"].iloc[-30]) if len(history) >= 30 else float(history["Total amount"].iloc[-1]),
                "rolling7": float(np.mean(last7)),
                "rolling30": float(np.mean(last30))
            }])

            pred_val = max(0.0, float(rf_model.predict(feat)[0]))
            preds.append({
                "Date": future_date.strftime("%Y-%m-%d"),
                "Predicted Sales": round(pred_val, 2),
                "Confidence": "High" if step <= 7 else "Medium"
            })
            history.loc[len(history)] = [future_date, pred_val]

        return pd.DataFrame(preds)
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

        # 1. Remote API with rapid retry
        response = None
        for attempt in range(3):
            try:
                timeout = 2.5 if attempt == 0 else 10
                response = requests.post(
                    f"{BASE_URL}/predict",
                    files=files,
                    timeout=timeout
                )
                if response.status_code == 200:
                    break
            except Exception:
                pass

        if response is not None and response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return pd.DataFrame(data)
            if isinstance(data, dict):
                if "error" not in data:
                    return pd.DataFrame([data])
    except Exception:
        pass

    # 2. Local Trained ML Fallback
    local_df = _local_forecast_from_csv(uploaded_file)
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

        # 1. Remote API with retry loop
        response = None
        for attempt in range(3):
            try:
                timeout = 2.5 if attempt == 0 else 10
                response = requests.post(
                    f"{BASE_URL}/forecast-backtest",
                    files=files,
                    timeout=timeout
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

    # 2. Local Trained ML Fallback
    local_res = _local_backtest_from_csv(uploaded_file)
    if local_res is not None:
        return local_res

    return {
        "results": pd.DataFrame(),
        "metrics": {},
        "period": {},
        "error": "Unable to complete forecast backtest. Please check that your CSV has 'Order Date' and 'Total amount' columns."
    }