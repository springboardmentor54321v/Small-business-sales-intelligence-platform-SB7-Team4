from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# =====================================================
# Revenue API
# =====================================================

def test_revenue_api():

    response = client.get("/revenue/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_revenue" in data
    assert "total_outstanding" in data
    assert "daily_collections" in data


# =====================================================
# Notification API
# =====================================================

def test_notification_api():

    response = client.get("/notifications")

    assert response.status_code == 200

    data = response.json()

    assert "total_notifications" in data
    assert "notifications" in data


# =====================================================
# Inventory API
# =====================================================

def test_inventory_api():

    response = client.get("/inventory/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Sales Transaction API
# =====================================================

def test_sales_transaction_api():

    response = client.get("/sales/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Invoice API
# =====================================================

def test_invoice_api():

    response = client.get("/invoices/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Customer API
# =====================================================

def test_customer_api():

    response = client.get("/customers/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Payment API
# =====================================================

def test_payment_api():

    response = client.get("/payments/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
