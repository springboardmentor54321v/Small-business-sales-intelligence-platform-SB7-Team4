import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load customer segmentation data
customer_df = pd.read_csv("AIML/week2/customer_grouping/customer_segments.csv")

# Load trained K-Means model
model = joblib.load("AIML/week2/customer_grouping/kmeans_customer_model.pkl")

# Cluster name mapping
cluster_names = {
    0: "High-Value Customers",
    1: "Regular Customers",
    2: "Low-Value Customers",
}


@app.route("/")
def home():
    return jsonify(
        {"message": "Customer Grouping API is running.", "endpoint": "/customer-group"}
    )


@app.route("/customer-group", methods=["POST"])
def customer_group():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received."}), 400

    if "Customer ID" not in data:
        return jsonify({"error": "Customer ID is required."}), 400

    customer_id = data["Customer ID"]

    customer = customer_df[customer_df["Customer ID"] == customer_id]

    if customer.empty:
        return jsonify({"error": "Customer ID not found."}), 404

    cluster = int(customer.iloc[0]["Cluster"])

    return jsonify(
        {"Customer ID": customer_id, "Customer Group": cluster_names[cluster]}
    )


if __name__ == "__main__":
    app.run(debug=True)
