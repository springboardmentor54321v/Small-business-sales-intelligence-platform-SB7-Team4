import pandas as pd

def create_features(df):

    # Convert Order Date to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Sort by date
    df = df.sort_values("Order Date").reset_index(drop=True)

    # Date-based features
    df["day"] = df["Order Date"].dt.day
    df["month"] = df["Order Date"].dt.month
    df["year"] = df["Order Date"].dt.year
    df["dayofweek"] = df["Order Date"].dt.dayofweek
    df["weekofyear"] = df["Order Date"].dt.isocalendar().week.astype(int)
    df["quarter"] = df["Order Date"].dt.quarter

    # Lag features
    df["lag1"] = df["Total amount"].shift(1)
    df["lag7"] = df["Total amount"].shift(7)
    df["lag30"] = df["Total amount"].shift(30)

    # Rolling mean features
    df["rolling7"] = df["Total amount"].rolling(7).mean()
    df["rolling30"] = df["Total amount"].rolling(30).mean()

    # Remove rows containing NaN values
    df = df.dropna().reset_index(drop=True)

    return df