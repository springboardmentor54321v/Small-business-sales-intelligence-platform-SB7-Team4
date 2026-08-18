import requests
import pandas as pd

from config.config import AUTH_BASE_URL as BASE_URL


def get_recommendations(product_name):

    if not product_name or not product_name.strip():
        return pd.DataFrame(
            columns=["Rank", "Product", "CoOccurrence"]
        )

    try:
        import time
        response = None
        for attempt in range(4):
            try:
                timeout = 3 if attempt == 0 else 60
                if attempt > 0:
                    st.info(f"⏳ Connection attempt {attempt}/3 to the AI Recommendation engine (Render is waking up)...")
                response = requests.post(
                    f"{BASE_URL}/recommend-product",
                    json={
                        "Product Name": product_name.strip()
                    },
                    timeout=timeout
                )
                if response.status_code not in [502, 503]:
                    break
                time.sleep(3)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt == 3:
                    raise
                time.sleep(3)

        if response is None:
            raise requests.exceptions.RequestException("Failed to contact Recommendation engine.")

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