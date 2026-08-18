import os
import requests
import pandas as pd
import numpy as np
import streamlit as st
import joblib

from config.config import AUTH_BASE_URL as BASE_URL


def _local_churn_prediction(customer_id):
    """Executes the exact trained Random Forest Churn model from AIML/week3/churn_prediction/churn_model.pkl."""
    try:
        model_path = "AIML/week3/churn_prediction/churn_model.pkl"
        if not os.path.exists(model_path):
            for alt in ["../" + model_path, "../../" + model_path]:
                if os.path.exists(alt):
                    model_path = alt
                    break

        if not os.path.exists(model_path):
            return None

        churn_model = joblib.load(model_path)

        data_paths = [
            "AIML/week1/preprocessing/cleaned_dataset.csv",
            "../AIML/week1/preprocessing/cleaned_dataset.csv",
            "Backend_Database/app/etl/output/sales_transactions.csv",
            "../Backend_Database/app/etl/output/sales_transactions.csv"
        ]
        df = pd.DataFrame()
        for p in data_paths:
            if os.path.exists(p):
                try:
                    df = pd.read_csv(p)
                    break
                except Exception:
                    pass

        if df.empty:
            return None

        col_map = {}
        for c in df.columns:
            norm = c.strip().lower()
            if "customer" in norm and "id" in norm:
                col_map[c] = "Customer ID"
            elif "total" in norm or "amount" in norm or "sales" in norm:
                col_map[c] = "Total amount"
            elif "order" in norm and "date" in norm:
                col_map[c] = "Order Date"
            elif "profit" in norm:
                col_map[c] = "Profit"
            elif "quantity" in norm or "qty" in norm:
                col_map[c] = "Quantity"
            elif "order" in norm and "id" in norm:
                col_map[c] = "Order ID"
        df = df.rename(columns=col_map)

        if "Customer ID" not in df.columns:
            return None

        cust = df[df["Customer ID"].astype(str).str.strip().str.upper() == str(customer_id).strip().upper()]
        if cust.empty:
            return {
                "Customer ID": customer_id,
                "Risk": "Low Risk",
                "Risk Score": 0.08,
                "Total Orders": 0,
                "Total Revenue": 0.0,
                "Last Purchase Date": "New Account",
                "Days Since Last Purchase": 0,
                "Risk Factors": ["New customer account with no historical churn risk signals."],
                "Prescriptive Actions": ["Deliver welcome onboarding email with first-order incentive."]
            }

        freq = len(cust["Order ID"].unique()) if "Order ID" in cust.columns else len(cust)
        spend = float(pd.to_numeric(cust["Total amount"], errors="coerce").fillna(0).sum())
        profit = float(pd.to_numeric(cust["Profit"], errors="coerce").fillna(spend * 0.25).sum()) if "Profit" in cust.columns else spend * 0.25
        qty = float(pd.to_numeric(cust["Quantity"], errors="coerce").fillna(3.0).mean()) if "Quantity" in cust.columns else 3.0

        if "Order Date" in cust.columns:
            dates = pd.to_datetime(cust["Order Date"], dayfirst=True, errors="coerce").dropna().sort_values()
            all_dates = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce").dropna()
            max_date = all_dates.max() if not all_dates.empty else pd.Timestamp.now()
            last_date = dates.max() if not dates.empty else max_date
            first_date = dates.min() if not dates.empty else last_date
            lifespan = max(1.0, float((last_date - first_date).days))
            days_since = max(0, int((max_date - last_date).days))
            last_purchase_str = last_date.strftime("%Y-%m-%d")
        else:
            lifespan = 180.0
            days_since = 30
            last_purchase_str = "N/A"

        avg_gap = max(1.0, float(lifespan / max(1, freq)))
        recency_gap_ratio = float(days_since / max(1.0, avg_gap))
        order_rate = float(freq / max(1.0, lifespan / 30.0))
        spend_rate = float(spend / max(1.0, lifespan / 30.0))
        margin = float(profit / max(1.0, spend))
        aov = float(spend / max(1, freq))

        feat = pd.DataFrame([{
            "PurchaseFrequency": freq,
            "TotalSpending": spend,
            "AverageOrderValue": aov,
            "CustomerLifespanDays": lifespan,
            "AvgDaysBetweenOrders": avg_gap,
            "TotalProfit": profit,
            "AvgQuantity": qty,
            "RecencyVsAvgGap": recency_gap_ratio,
            "OrderRatePerMonth": order_rate,
            "SpendPerMonth": spend_rate,
            "ProfitMargin": margin
        }])

        proba = churn_model.predict_proba(feat)[0]
        churn_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

        if churn_prob >= 0.70:
            risk = "High Risk"
            factors = [
                f"Long inactivity ({days_since} days since last order)",
                f"Recency-to-gap ratio ({recency_gap_ratio:.2f}x historical average gap)"
            ]
            actions = [
                "Trigger urgent win-back discount offer (15-20% off)",
                "Assign dedicated relationship manager for direct outreach"
            ]
        elif churn_prob >= 0.40:
            risk = "Medium Risk"
            factors = [
                f"Moderate inactivity window ({days_since} days)",
                f"Order frequency is moderate ({freq} orders)"
            ]
            actions = [
                "Send personalized product recommendation re-engagement email",
                "Enroll customer in loyalty rewards tier"
            ]
        else:
            risk = "Low Risk"
            factors = [
                f"Active order activity ({freq} orders, ₹{spend:,.2f} total spend)",
                "Consistent order velocity within historical norms"
            ]
            actions = [
                "Maintain standard VIP loyalty engagement",
                "Cross-sell premium accessories and new product arrivals"
            ]

        return {
            "Customer ID": customer_id,
            "Risk": risk,
            "Risk Score": round(churn_prob, 4),
            "Total Orders": freq,
            "Total Revenue": round(spend, 2),
            "Last Purchase Date": last_purchase_str,
            "Days Since Last Purchase": days_since,
            "Risk Factors": factors,
            "Prescriptive Actions": actions
        }
    except Exception:
        return None


def get_churn_risk(customer_id="AA-10315"):

    payload = {
        "Customer ID": customer_id
    }

    # 1. Try remote backend API
    try:
        response = None
        for attempt in range(2):
            try:
                response = requests.post(
                    f"{BASE_URL}/churn-risk",
                    json=payload,
                    timeout=3
                )
                if response.status_code == 200:
                    break
            except Exception:
                pass

        if response is not None and response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                return pd.DataFrame([data])
            if isinstance(data, list):
                return pd.DataFrame(data)
    except Exception:
        pass

    # 2. Local Trained Churn Model
    local_res = _local_churn_prediction(customer_id)
    if local_res:
        return pd.DataFrame([local_res])

    return pd.DataFrame({
        "Message": ["No churn prediction found."]
    })