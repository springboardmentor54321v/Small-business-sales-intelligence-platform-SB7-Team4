from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("stub_service/lightgbm_daily_model.pkl")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "MarketMind AI Sales Forecast API",
        "disclaimer": [
            "Upload a CSV file using POST /predict.",
            "The CSV must contain the following columns:",
            "1. Order Date",
            "2. Total amount",
            "Order Date must contain valid dates.",
            "Total amount must contain numeric values only.",
            "The dataset should contain at least 30 days of historical sales data.",
            "Missing values are not allowed in required columns.",
            "The API forecasts sales for the next 30 days."
        ]
    })


@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["file"]

    df = pd.read_csv(file) #type: ignore

    df = df[["Order Date", "Total amount"]]

    df["Order Date"] = pd.to_datetime(df["Order Date"])


    df = (
        df.groupby("Order Date")["Total amount"]
        .sum()
        .reset_index()
        .sort_values("Order Date")
        .reset_index(drop=True)
    )

    history = df.copy()
    if len(history) < 30:
        return jsonify({
        "error": "Insufficient historical data.",
        "message": "At least 30 days of historical sales data are required to generate a 30-day forecast."
    }), 400
    

    predictions = []

    for i in range(30):

        future_date = history["Order Date"].max() + pd.Timedelta(days=1)

        lag1 = history["Total amount"].iloc[-1]
        lag7 = history["Total amount"].iloc[-7]
        lag30 = history["Total amount"].iloc[-30]

        rolling7 = history["Total amount"].tail(7).mean()
        rolling30 = history["Total amount"].tail(30).mean()

        row = pd.DataFrame({
            "day": [future_date.day],
            "month": [future_date.month],
            "year": [future_date.year],
            "dayofweek": [future_date.dayofweek],
            "weekofyear": [int(future_date.isocalendar().week)],
            "quarter": [future_date.quarter],
            "lag1": [lag1],
            "lag7": [lag7],
            "lag30": [lag30],
            "rolling7": [rolling7],
            "rolling30": [rolling30]
        })

        pred = float(model.predict(row)[0])

        predictions.append({
            "Order Date": future_date.strftime("%Y-%m-%d"),
            "Predicted Sales": round(pred, 2)
        })

        history.loc[len(history)] = [future_date, pred]

    return jsonify(predictions)


if __name__ == "__main__":
    app.run(debug=True)