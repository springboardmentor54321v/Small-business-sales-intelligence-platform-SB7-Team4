import pandas as pd


def get_sales_forecast():
    """
    Dummy sales forecast data.
    Replace with ML model/API later.
    """

    forecast = [

        {"Month": "Jan", "Predicted Sales": 120000},
        {"Month": "Feb", "Predicted Sales": 145000},
        {"Month": "Mar", "Predicted Sales": 162000},
        {"Month": "Apr", "Predicted Sales": 181000},
        {"Month": "May", "Predicted Sales": 210000},
        {"Month": "Jun", "Predicted Sales": 235000},
        {"Month": "Jul", "Predicted Sales": 260000},
        {"Month": "Aug", "Predicted Sales": 290000},
        {"Month": "Sep", "Predicted Sales": 315000},
        {"Month": "Oct", "Predicted Sales": 340000},
        {"Month": "Nov", "Predicted Sales": 365000},
        {"Month": "Dec", "Predicted Sales": 395000}

    ]

    return pd.DataFrame(forecast)