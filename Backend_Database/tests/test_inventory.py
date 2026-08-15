from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# =====================================================
# Get All Inventory
# =====================================================

def test_get_inventory():

    response = client.get("/inventory/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Inventory Search By Product ID
# =====================================================

def test_inventory_search_by_product_id():

    response = client.get(
        "/inventory/",
        params={
            "search": "FUR-TA-10003627"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Inventory Search By Product Name
# =====================================================

def test_inventory_search_by_product_name():

    response = client.get(
        "/inventory/",
        params={
            "search": "Bevis Conference Table"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Inventory Category Filter
# =====================================================

def test_inventory_category_filter():

    response = client.get(
        "/inventory/",
        params={
            "category": "Furniture"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# Get Inventory By Product ID
# =====================================================

def test_get_inventory_by_product_id():

    response = client.get("/inventory/")

    assert response.status_code == 200

    data = response.json()

    if data:

        product_id = data[0]["product_id"]

        detail_response = client.get(
            f"/inventory/{product_id}"
        )

        assert detail_response.status_code == 200

        inventory = detail_response.json()

        assert inventory["product_id"] == product_id
