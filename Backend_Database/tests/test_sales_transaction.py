from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# =====================================================
# Get Sales Transactions
# =====================================================

def test_get_sales_transactions():

    response = client.get("/sales/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =====================================================
# Get Sales Transaction By ID
# =====================================================

def test_get_sales_transaction_by_id():

    response = client.get("/sales/")

    assert response.status_code == 200

    data = response.json()

    if data:

        transaction_id = data[0]["transaction_id"]

        detail_response = client.get(
            f"/sales/{transaction_id}"
        )

        assert detail_response.status_code == 200

        transaction = detail_response.json()

        assert transaction["transaction_id"] == transaction_id
