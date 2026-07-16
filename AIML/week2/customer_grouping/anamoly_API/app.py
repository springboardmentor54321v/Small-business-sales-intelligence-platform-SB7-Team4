import os

import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load anomaly detection results
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "anomaly_detection_results.csv")

anomaly_df = pd.read_csv(csv_path)


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {"message": "Anomaly Detection API is running.", "endpoint": "/check-anomaly"}
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
    app.run(debug=True)
