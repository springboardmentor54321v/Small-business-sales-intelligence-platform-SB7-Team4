import os

import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load churn data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "churn_risk", "customer_churn.csv")
customer_df = pd.read_csv(csv_path)


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {"message": "Customer Churn Risk API is running.", "endpoint": "/churn-risk"}
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

    return jsonify({"Customer ID": customer_id, "Risk": customer.iloc[0]["Risk"]})


if __name__ == "__main__":
    app.run(debug=True)
