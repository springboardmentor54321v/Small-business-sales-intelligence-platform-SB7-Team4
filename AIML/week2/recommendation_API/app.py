import os

import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load recommendation data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "product_recommendations.csv")

recommendation_df = pd.read_csv(csv_path)


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "message": "Product Recommendation API is running.",
            "endpoint": "/recommend-product",
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
        {"Product Name": data["Product Name"], "Recommendations": recommendations}
    )


if __name__ == "__main__":
    app.run(debug=True)
