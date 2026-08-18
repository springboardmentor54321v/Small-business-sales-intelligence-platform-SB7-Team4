import requests
import pandas as pd

from config.config import AUTH_BASE_URL as BASE_URL


def get_recommendations(product_name):

    if not product_name or not product_name.strip():
        return pd.DataFrame(
            columns=["Rank", "Product", "CoOccurrence"]
        )

    try:
        import streamlit as st
        try:
            response = requests.post(
                f"{BASE_URL}/recommend-product",
                json={
                    "Product Name": product_name.strip()
                },
                timeout=3
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            st.info("⏳ The AI Recommendation engine is currently waking up on Render. Performing analysis (up to 60 seconds)...")
            response = requests.post(
                f"{BASE_URL}/recommend-product",
                json={
                    "Product Name": product_name.strip()
                },
                timeout=60
            )

        if response.status_code in [502, 503]:
            st.info("⏳ Establishing connection to the AI recommendation engine (up to 60 seconds)...")
            response = requests.post(
                f"{BASE_URL}/recommend-product",
                json={
                    "Product Name": product_name.strip()
                },
                timeout=60
            )

        if response.status_code == 404:
            data = response.json()

            return pd.DataFrame({
                "Error": [
                    data.get("error", "Product not found.")
                ]
            })

        response.raise_for_status()

        data = response.json()

        recommendations = data.get("Recommendations", [])

        rows = []

        for rank, item in enumerate(recommendations, start=1):
            rows.append({
                "Rank": rank,
                "Product": item.get("Product", ""),
                "CoOccurrence": item.get("CoOccurrence", 0)
            })

        return pd.DataFrame(rows)

    except requests.exceptions.RequestException as e:

        return pd.DataFrame({
            "Error": [f"API Error: {e}"]
        })

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })