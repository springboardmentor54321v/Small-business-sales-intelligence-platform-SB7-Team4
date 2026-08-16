from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# =====================================================
# Get All Payments
# =====================================================

def test_get_payments():

    response = client.get("/payments/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =====================================================
# Get Payment By ID
# =====================================================

def test_get_payment_by_id():

    response = client.get("/payments/")

    assert response.status_code == 200

    data = response.json()

    if data:

        payment_id = data[0]["payment_id"]

        detail_response = client.get(
            f"/payments/{payment_id}"
        )

        assert detail_response.status_code == 200

        payment = detail_response.json()

        assert payment["payment_id"] == payment_id
