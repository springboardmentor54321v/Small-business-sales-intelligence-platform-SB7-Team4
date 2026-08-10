import os

import joblib
import pandas as pd
from flask import Flask, jsonify, request


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# FORECASTING
# ============================================================

forecast_model_path = os.path.join(
    BASE_DIR,
    "..",
    "week3",
    "forecasting",
    "catboost",
    "catboost_daily_model.pkl",
)

model = joblib.load(forecast_model_path)


# ============================================================
# CUSTOMER GROUPING
# ============================================================

group_csv_path = os.path.join(
    BASE_DIR,
    "..",
    "week3",
    "customer_grouping",
    "customer_segment.csv",
)

group_df = pd.read_csv(group_csv_path)

cluster_names = {
    0: "High-Value Customers",
    1: "Regular Customers",
    2: "Low-Value Customers",
}


# ============================================================
# CHURN RISK - MILESTONE 3
# ============================================================

churn_csv_path = os.path.join(
    BASE_DIR,
    "..",
    "week3",
    "churn_prediction",
    "churn_customers.csv",
)

customer_df = pd.read_csv(churn_csv_path)


# ============================================================
# PRODUCT RECOMMENDATION
# ============================================================

recommendation_csv_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "week3",
    "product_recommendation",
    "product_recommendations.csv",
)

recommendation_df = pd.read_csv(recommendation_csv_path)


# ============================================================
# ANOMALY DETECTION
# ============================================================

anomaly_csv_path = os.path.join(
    BASE_DIR,
    "..",
    "week3",
    "anomaly_detection",
    "anomaly_detection_results.csv",
)

anomaly_df = pd.read_csv(anomaly_csv_path)


# ============================================================
# HOME
# ============================================================


@app.route("/", methods=["GET"])
def home():

    return jsonify(
        {
            "project": "MarketMind AI APIs",
            "available_apis": {
                "forecast": {
                    "endpoint": "/predict",
                    "method": "POST",
                },
                "customer_grouping": {
                    "endpoint": "/customer-group",
                    "method": "POST",
                },
                "churn_risk": {
                    "endpoint": "/churn-risk",
                    "method": "POST",
                },
                "product_recommendation": {
                    "endpoint": "/recommend-product",
                    "method": "POST",
                },
                "anomaly_detection": {
                    "endpoint": "/check-anomaly",
                    "method": "POST",
                },
            },
        }
    )


# ============================================================
# SALES FORECASTING API
# ============================================================


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]

    file.stream.seek(0)

    df = pd.read_csv(file.stream)

    required_columns = [
        "Order Date",
        "Total amount",
    ]

    for col in required_columns:
        if col not in df.columns:
            return jsonify({"error": f"Missing column: {col}"}), 400

    df = df[required_columns].copy()

    df["Order Date"] = df["Order Date"].astype(str).str.strip()

    df["Total amount"] = pd.to_numeric(
        df["Total amount"],
        errors="coerce",
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True,
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "Order Date",
            "Total amount",
        ]
    )

    if df.empty:
        return jsonify({"error": "Uploaded file contains no valid data."}), 400

    history = df.sort_values("Order Date").reset_index(drop=True)

    if len(history) < 30:
        return jsonify(
            {
                "error": "Insufficient historical data.",
                "message": "At least 30 valid days of historical "
                "sales data are required.",
            }
        ), 400

    predictions = []

    for _ in range(30):
        future_date = history["Order Date"].iloc[-1] + pd.Timedelta(days=1)

        row = pd.DataFrame(
            {
                "day": [future_date.day],
                "month": [future_date.month],
                "year": [future_date.year],
                "dayofweek": [future_date.dayofweek],
                "weekofyear": [future_date.isocalendar().week],
                "quarter": [future_date.quarter],
                "lag1": [history["Total amount"].iloc[-1]],
                "lag7": [history["Total amount"].iloc[-7]],
                "lag30": [history["Total amount"].iloc[-30]],
                "rolling7": [history["Total amount"].tail(7).mean()],
                "rolling30": [history["Total amount"].tail(30).mean()],
            }
        )

        prediction = float(model.predict(row)[0])

        recent_sales = history["Total amount"].tail(30)

        recent_mean = recent_sales.mean()

        recent_std = recent_sales.std()

        difference = abs(prediction - recent_mean)

        if difference <= recent_std:
            confidence = "High"

        elif difference <= 2 * recent_std:
            confidence = "Medium"

        else:
            confidence = "Low"

        predictions.append(
            {
                "Order Date": future_date.strftime("%Y-%m-%d"),
                "Predicted Sales": round(prediction, 2),
                "Confidence": confidence,
            }
        )

        history.loc[len(history)] = [
            future_date,
            prediction,
        ]

    return jsonify(predictions)


# ============================================================
# CUSTOMER GROUPING API
# ============================================================


@app.route("/customer-group", methods=["POST"])
def customer_group():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Customer ID" not in data:
        return jsonify({"error": "Customer ID is required."}), 400

    customer_id = str(data["Customer ID"]).strip()

    customer = group_df[group_df["Customer ID"].astype(str).str.strip() == customer_id]

    if customer.empty:
        return jsonify({"error": "Customer ID not found."}), 404

    cluster = int(customer.iloc[0]["Cluster"])

    customer_group_name = cluster_names.get(
        cluster,
        "Unknown Customer Group",
    )

    return jsonify(
        {
            "Customer ID": customer_id,
            "Customer Group": customer_group_name,
        }
    )


# ============================================================
# CHURN RISK API - MILESTONE 3
# ============================================================


@app.route("/churn-risk", methods=["POST"])
def churn_risk():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Customer ID" not in data:
        return jsonify({"error": "Customer ID is required."}), 400

    customer_id = str(data["Customer ID"]).strip()

    customer = customer_df[
        customer_df["Customer ID"].astype(str).str.strip() == customer_id
    ]

    if customer.empty:
        return jsonify({"error": "Customer ID not found."}), 404

    customer_record = customer.iloc[0]

    return jsonify(
        {
            "Customer ID": customer_id,
            "Risk": str(customer_record["Risk"]),
            "Risk Score": round(float(customer_record["PredictedChurnProb"]), 4),
            "Total Orders": int(customer_record["PurchaseFrequency"]),
            "Total Revenue": round(float(customer_record["TotalSpending"]), 2),
            "Last Purchase Date": str(customer_record["LastPurchaseDate"]),
            "Days Since Last Purchase": int(customer_record["DaysSinceLastPurchase"]),
        }
    )


# ============================================================
# PRODUCT RECOMMENDATION API
# ============================================================


@app.route("/recommend-product", methods=["POST"])
def recommend_product():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Product Name" not in data:
        return jsonify({"error": "Product Name is required."}), 400

    product_name = str(data["Product Name"]).strip().lower()

    recommendations = recommendation_df[
        recommendation_df["Product Name"].str.lower() == product_name
    ].sort_values(by="CoOccurrence", ascending=False)

    if recommendations.empty:
        return jsonify({"error": "Product not found."}), 404

    return jsonify(
        {
            "Product Name": data["Product Name"],
            "Recommendations": [
                {
                    "Product": row["Recommended Product"],
                    "CoOccurrence": row["CoOccurrence"],
                }
                for _, row in recommendations.iterrows()
            ],
        }
    )


# ============================================================
# ANOMALY DETECTION API
# ============================================================


@app.route("/check-anomaly", methods=["POST"])
def check_anomaly():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Order Date" not in data:
        return jsonify({"error": "Order Date is required."}), 400

    order_date = str(data["Order Date"]).strip()

    result = anomaly_df[anomaly_df["Order Date"].astype(str).str.strip() == order_date]

    if result.empty:
        return jsonify({"error": "Order Date not found."}), 404

    record = result.iloc[0]

    return jsonify(
        {
            "Order Date": record["Order Date"],
            "Total Sales": float(record["Total amount"]),
            "Anomaly": bool(record["Anomaly"]),
        }
    )


@app.route("/forecast-backtest", methods=["POST"])
def forecast_backtest():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]

    file.stream.seek(0)

    df = pd.read_csv(file.stream)

    required_columns = [
        "Order Date",
        "Total amount",
    ]

    for col in required_columns:
        if col not in df.columns:
            return jsonify({"error": f"Missing column: {col}"}), 400

    df = df[required_columns].copy()

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")

    df["Total amount"] = pd.to_numeric(df["Total amount"], errors="coerce")

    df = df.dropna(subset=["Order Date", "Total amount"])

    if df.empty:
        return jsonify({"error": "Uploaded file contains no valid data."}), 400

    # Aggregate transactions into daily sales
    daily_sales = (
        df.groupby("Order Date")["Total amount"]
        .sum()
        .reset_index()
        .sort_values("Order Date")
        .reset_index(drop=True)
    )

    if len(daily_sales) < 60:
        return jsonify(
            {
                "error": "Insufficient historical data.",
                "message": "At least 60 daily observations are required.",
            }
        ), 400

    # --------------------------------------------------------
    # Historical test period
    # Last 30 available dates are used for backtesting
    # --------------------------------------------------------

    test_size = 30

    train_data = daily_sales.iloc[:-test_size].copy()

    test_data = daily_sales.iloc[-test_size:].copy()

    history = train_data.copy()

    predictions = []

    # --------------------------------------------------------
    # Generate historical predictions
    # --------------------------------------------------------

    for _, actual_row in test_data.iterrows():
        prediction_date = actual_row["Order Date"]

        row = pd.DataFrame(
            {
                "day": [prediction_date.day],
                "month": [prediction_date.month],
                "year": [prediction_date.year],
                "dayofweek": [prediction_date.dayofweek],
                "weekofyear": [prediction_date.isocalendar().week],
                "quarter": [prediction_date.quarter],
                "lag1": [history["Total amount"].iloc[-1]],
                "lag7": [history["Total amount"].iloc[-7]],
                "lag30": [history["Total amount"].iloc[-30]],
                "rolling7": [history["Total amount"].tail(7).mean()],
                "rolling30": [history["Total amount"].tail(30).mean()],
            }
        )

        prediction = float(model.predict(row)[0])

        predictions.append(
            {
                "Order Date": prediction_date.strftime("%Y-%m-%d"),
                "Actual Sales": round(float(actual_row["Total amount"]), 2),
                "Predicted Sales": round(prediction, 2),
            }
        )

        # ----------------------------------------------------
        # IMPORTANT:
        # For historical backtesting, use the ACTUAL value
        # to move the history forward.
        # ----------------------------------------------------

        history.loc[len(history)] = [prediction_date, actual_row["Total amount"]]

        # ========================================================
    # BACKTEST EVALUATION
    # ========================================================

    # ========================================================
    # BACKTEST EVALUATION
    # ========================================================

    actual_values = [item["Actual Sales"] for item in predictions]

    predicted_values = [item["Predicted Sales"] for item in predictions]

    # MAE
    mae = sum(
        abs(actual - predicted)
        for actual, predicted in zip(actual_values, predicted_values)
    ) / len(actual_values)

    # RMSE
    rmse = (
        sum(
            (actual - predicted) ** 2
            for actual, predicted in zip(actual_values, predicted_values)
        )
        / len(actual_values)
    ) ** 0.5

    # MAPE
    percentage_errors = [
        abs((actual - predicted) / actual) * 100
        for actual, predicted in zip(actual_values, predicted_values)
        if actual != 0
    ]

    mape = sum(percentage_errors) / len(percentage_errors) if percentage_errors else 0

    # ========================================================
    # RETURN BACKTEST RESULTS
    # ========================================================

    return jsonify(
        {
            "Backtest Period": {
                "Start": test_data["Order Date"].min().strftime("%Y-%m-%d"),
                "End": test_data["Order Date"].max().strftime("%Y-%m-%d"),
            },
            "Number of Days": len(predictions),
            "Evaluation Metrics": {
                "MAE": round(mae, 2),
                "RMSE": round(rmse, 2),
                "MAPE": round(mape, 2),
            },
            "Results": predictions,
        }
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
    )
