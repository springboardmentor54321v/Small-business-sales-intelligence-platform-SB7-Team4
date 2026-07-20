import pandas as pd


def get_recommendations():
    """
    Sample AI Product Recommendation Model
    Replace this dummy data with ML predictions later.
    """

    recommendations = [

        {
            "Customer": "Ravi",
            "Last Purchase": "Laptop",
            "Recommended Product": "Mouse",
            "Confidence": 95,
            "Reason": "Frequently bought together"
        },

        {
            "Customer": "Priya",
            "Last Purchase": "Printer",
            "Recommended Product": "Ink Cartridge",
            "Confidence": 92,
            "Reason": "Consumable product"
        },

        {
            "Customer": "Rahul",
            "Last Purchase": "Keyboard",
            "Recommended Product": "Mouse Pad",
            "Confidence": 89,
            "Reason": "Similar customers purchased"
        },

        {
            "Customer": "Anita",
            "Last Purchase": "Monitor",
            "Recommended Product": "HDMI Cable",
            "Confidence": 91,
            "Reason": "Frequently bought together"
        },

        {
            "Customer": "Kiran",
            "Last Purchase": "Laptop",
            "Recommended Product": "Laptop Bag",
            "Confidence": 90,
            "Reason": "Common follow-up purchase"
        }

    ]

    return pd.DataFrame(recommendations)