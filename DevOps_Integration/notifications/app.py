import os
from flask import Flask, jsonify

app = Flask(__name__)

# Mock database records for alerts
mock_notifications = [
    {
        "id": 1,
        "type": "low_stock",
        "message": "Product 'Mouse' is low on stock (Quantity: 3).",
        "created_at": "2026-07-27T12:00:00Z"
    },
    {
        "id": 2,
        "type": "overdue_invoice",
        "message": "Invoice INV-M2-01 has passed due date.",
        "created_at": "2026-07-27T12:05:00Z"
    },
    {
        "id": 3,
        "type": "low_stock",
        "message": "Product 'Keyboard' is low on stock (Quantity: 4).",
        "created_at": "2026-07-27T14:30:00Z"
    }
]

@app.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify(mock_notifications)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"service": "Notifications Service", "status": "running"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
