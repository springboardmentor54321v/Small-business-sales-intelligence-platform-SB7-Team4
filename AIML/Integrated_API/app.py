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
    "customer_churn_milestone3.csv",
)

customer_df = pd.read_csv(churn_csv_path)


# ============================================================
# PRODUCT RECOMMENDATION
# ============================================================

recommendation_csv_path = os.path.join(
    BASE_DIR,
    "..",
    "week2",
    "recommendation_API",
    "product_recommendations.csv",
)

recommendation_df = pd.read_csv(recommendation_csv_path)


# ============================================================
# ANOMALY DETECTION
# ============================================================

anomaly_csv_path = os.path.join(
    BASE_DIR,
    "..",
    "week2",
    "anamoly_API",
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
            "Risk": customer_record["Risk"],
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

    recommendations = []

    for _, row in recommendation_df.iterrows():
        pair = str(row["Product Pair"])

        pair = pair.replace("(", "").replace(")", "").replace("'", "")

        products = [product.strip() for product in pair.split(",")]

        if len(products) != 2:
            continue

        product1 = products[0].lower()
        product2 = products[1].lower()

        if product_name == product1:
            recommendations.append(products[1])

        elif product_name == product2:
            recommendations.append(products[0])

    recommendations = list(dict.fromkeys(recommendations))

    if not recommendations:
        return jsonify({"error": "Product not found."}), 404

    return jsonify(
        {
            "Product Name": data["Product Name"],
            "Recommendations": recommendations,
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


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
    )
