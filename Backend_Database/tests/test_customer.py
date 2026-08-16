from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# =====================================================
# Get Customers
# =====================================================

def test_get_customers():

    response = client.get("/customers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =====================================================
# Customer Search
# =====================================================

def test_customer_search():

    response = client.get(
        "/customers/",
        params={
            "search": "RH-19495"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
