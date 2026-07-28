import os

import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load forecasting model
model = joblib.load(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "week3",
        "forecasting",
        "catboost",
        "catboost_daily_model.pkl",
    )
)

# Customer Grouping
group_csv_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "week2",
    "customer_grouping",
    "customer_segments.csv",
)

group_df = pd.read_csv(group_csv_path)

cluster_names = {
    0: "High-Value Customers",
    1: "Regular Customers",
    2: "Low-Value Customers",
}

# Churn Risk
churn_csv_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "week2",
    "churn_risk",
    "customer_churn.csv",
)

customer_df = pd.read_csv(churn_csv_path)

# Product Recommendation
recommendation_csv_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "week2",
    "recommendation_API",
    "product_recommendations.csv",
)

recommendation_df = pd.read_csv(recommendation_csv_path)


# Load anomaly detection results
anomaly_csv_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "week2",
    "anamoly_API",
    "anomaly_detection_results.csv",
)

anomaly_df = pd.read_csv(anomaly_csv_path)


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "project": "MarketMind AI APIs",
            "forecast_api": "/predict",
            "method": "POST",
            "upload_file": "daily_sales.csv",
            "required_columns": ["Order Date", "Total amount"],
            "forecast": "Next 30 days",
        }
    )


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]
    file.stream.seek(0)  # Reset the file stream position to the beginning

    df = pd.read_csv(file.stream)
    print("Rows in uploaded file:", len(df))
    print(df.tail(5))

    # Check required columns
    required_columns = ["Order Date", "Total amount"]
    for col in required_columns:
        if col not in df.columns:
            return jsonify({"error": f"Missing column: {col}"}), 400

    df = df[required_columns].copy()

    # Clean column values
    df["Order Date"] = df["Order Date"].astype(str).str.strip()
    df["Total amount"] = pd.to_numeric(df["Total amount"], errors="coerce")

    # Convert dates automatically
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")

    # Remove invalid rows instead of stopping the API
    df = df.dropna(subset=["Order Date", "Total amount"])

    if df.empty:
        return jsonify({"error": "Uploaded file contains no valid data."}), 400

    history = df.sort_values("Order Date").reset_index(drop=True)
    print(history.tail(30))
    print("last date in history:", history["Order Date"].max())

    if len(history) < 30:
        return jsonify(
            {
                "error": "Insufficient historical data.",
                "message": "At least 30 valid days of historical sales data are required.",
            }
        ), 400

    predictions = []

    for i in range(30):
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
        mae = 1606.96
        if mae < 1700:
            confidence = "High"
        elif mae < 2500:
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

        history.loc[len(history)] = [future_date, prediction]

    return jsonify(predictions)


@app.route("/customer-group", methods=["POST"])
def customer_group():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received."}), 400

    if "Customer ID" not in data:
        return jsonify({"error": "Customer ID is required."}), 400

    customer_id = data["Customer ID"]

    customer = group_df[group_df["Customer ID"] == customer_id]

    if customer.empty:
        return jsonify({"error": "Customer ID not found."}), 404

    cluster = int(customer.iloc[0]["Cluster"])

    return jsonify(
        {
            "Customer ID": customer_id,
            "Customer Group": cluster_names[cluster],
        }
    )


@app.route("/churn-risk", methods=["POST"])
def churn_risk():

    data = request.get_json()

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Customer ID" not in data:
        return jsonify({"error": "Customer ID is required."}), 400

    customer_id = data["Customer ID"]

    customer = customer_df[customer_df["Customer ID"] == customer_id]

    if customer.empty:
        return jsonify({"error": "Customer ID not found."}), 404

    return jsonify(
        {
            "Customer ID": customer_id,
            "Risk": customer.iloc[0]["Risk"],
        }
    )


@app.route("/recommend-product", methods=["POST"])
def recommend_product():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Product Name" not in data:
        return jsonify({"error": "Product Name is required."}), 400

    product_name = data["Product Name"].strip().lower()

    recommendations = []

    for _, row in recommendation_df.iterrows():
        pair = row["Product Pair"]

        pair = pair.replace("(", "").replace(")", "").replace("'", "")
        products = [p.strip() for p in pair.split(",")]

        if len(products) != 2:
            continue

        p1 = products[0].lower()
        p2 = products[1].lower()

        if product_name == p1:
            recommendations.append(products[1])
        elif product_name == p2:
            recommendations.append(products[0])

    if not recommendations:
        return jsonify({"error": "Product not found."}), 404

    return jsonify(
        {
            "Product Name": data["Product Name"],
            "Recommendations": recommendations,
        }
    )


@app.route("/check-anomaly", methods=["POST"])
def check_anomaly():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "No JSON data received."}), 400

    if "Order Date" not in data:
        return jsonify({"error": "Order Date is required."}), 400

    order_date = data["Order Date"]

    result = anomaly_df[anomaly_df["Order Date"] == order_date]

    if result.empty:
        return jsonify({"error": "Order Date not found."}), 404

    return jsonify(
        {
            "Order Date": result.iloc[0]["Order Date"],
            "Total Sales": float(result.iloc[0]["Total amount"]),
            "Anomaly": bool(result.iloc[0]["Anomaly"]),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
