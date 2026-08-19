from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

import pandas as pd
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.repositories.sales_transaction_repository import (
    bulk_import_sales,
)

from app.utils.sales_csv import (
    detect_and_map_columns,
)

from app.models.store import Store


router = APIRouter(
    prefix="/api/sales",
    tags=["Sales Upload"]
)


@router.post("/upload")
async def upload_sales_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload, validate, clean and import a sales CSV.

    Supported:
    - MarketMind cleaned sales dataset
    - MarketMind standardized sales CSV
    - Known sales CSV column aliases
    """

    # ---------------------------------------------
    # 1. File validation
    # ---------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    # ---------------------------------------------
    # 2. Read CSV
    # ---------------------------------------------

    try:

        dataframe = pd.read_csv(
            file.file
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV file: {str(e)}"
        )

    if dataframe.empty:

        raise HTTPException(
            status_code=400,
            detail="CSV file contains no data."
        )

    # ---------------------------------------------
    # 3. Detect + normalize + clean
    # ---------------------------------------------

    dataframe = detect_and_map_columns(
        dataframe
    )

    # ---------------------------------------------
    # 4. Resolve store
    # ---------------------------------------------

    if "store_id" not in dataframe.columns:

        stores = db.query(Store).all()
        default_store_id = stores[0].store_id if stores else "1"

        required_location = ["city", "state", "country"]
        has_location = all(col in dataframe.columns for col in required_location)

        if has_location and stores:
            store_map = {}
            for store in stores:
                if store.location:
                    store_map[store.location.strip().lower()] = store.store_id

            resolved_store_ids = []
            for _, row in dataframe.iterrows():
                loc_key = f"{str(row.get('city', '')).strip()}, {str(row.get('state', '')).strip()}, {str(row.get('country', '')).strip()}".lower()
                resolved_store_ids.append(store_map.get(loc_key, default_store_id))
            dataframe["store_id"] = resolved_store_ids
        else:
            dataframe["store_id"] = default_store_id

    # ---------------------------------------------
    # 5. Import
    # ---------------------------------------------

    result = bulk_import_sales(
        db=db,
        dataframe=dataframe,
    )

    # ---------------------------------------------
    # 6. Response
    # ---------------------------------------------

    return {
    "status": "success",
    "message":
        "Sales CSV validated, cleaned and "
        "imported successfully.",
    "filename": file.filename,
    "rows_received": len(dataframe),
    "rows_inserted":
        result["inserted_count"],
    "rows_skipped":
        result["skipped_count"],
    "invoices_created":
        result["created_invoice_count"],
    "invoice_items_created":
        result["created_item_count"],
    "columns": len(dataframe.columns),
    "column_names":
        dataframe.columns.tolist(),
}
