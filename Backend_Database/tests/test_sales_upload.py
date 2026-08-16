from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# =====================================================
# Sales Upload - Reject Non-CSV File
# =====================================================

def test_sales_upload_rejects_non_csv():

    response = client.post(
        "/api/sales/upload",
        files={
            "file": (
                "test.txt",
                BytesIO(b"this is not a csv"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Only CSV files are allowed."


# =====================================================
# Sales Upload - Reject Empty CSV
# =====================================================

def test_sales_upload_rejects_empty_csv():

    response = client.post(
        "/api/sales/upload",
        files={
            "file": (
                "empty.csv",
                BytesIO(b""),
                "text/csv",
            )
        },
    )

    assert response.status_code == 400


# =====================================================
# Sales Upload - Reject Invalid CSV Schema
# =====================================================

def test_sales_upload_rejects_invalid_csv_schema():

    csv_content = (
        "invalid_column_1,invalid_column_2\n"
        "value1,value2\n"
    )

    response = client.post(
        "/api/sales/upload",
        files={
            "file": (
                "invalid.csv",
                BytesIO(csv_content.encode()),
                "text/csv",
            )
        },
    )

    assert response.status_code == 400
