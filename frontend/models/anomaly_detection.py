import pandas as pd


def get_anomaly_alerts():
    """
    Dummy anomaly detection alerts.
    Replace with ML model/API later.
    """

    alerts = [

        {
            "Alert ID": "ALT001",
            "Type": "Unusual Sales Spike",
            "Store": "Vijayawada",
            "Severity": "High",
            "Status": "Open"
        },

        {
            "Alert ID": "ALT002",
            "Type": "Inventory Mismatch",
            "Store": "Guntur",
            "Severity": "Medium",
            "Status": "Investigating"
        },

        {
            "Alert ID": "ALT003",
            "Type": "Low Stock",
            "Store": "Hyderabad",
            "Severity": "High",
            "Status": "Open"
        },

        {
            "Alert ID": "ALT004",
            "Type": "Duplicate Invoice",
            "Store": "Visakhapatnam",
            "Severity": "Low",
            "Status": "Resolved"
        },

        {
            "Alert ID": "ALT005",
            "Type": "Payment Delay",
            "Store": "Chennai",
            "Severity": "Medium",
            "Status": "Open"
        }

    ]

    return pd.DataFrame(alerts)