from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

router = APIRouter(
    prefix="/api/sales",
    tags=["Sales Upload"]
)


@router.post("/upload")
async def upload_sales_csv(file: UploadFile = File(...)):
    """
    Upload and validate a sales CSV file.
    """

    # -------------------------------
    # Step 1: Validate file type
    # -------------------------------
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    # -------------------------------
    # Step 2: Read CSV safely
    # -------------------------------
    try:
        dataframe = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV file: {str(e)}"
        )

    # -------------------------------
    # Step 3: Normalize column names
    # -------------------------------
    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
    )

    # -------------------------------
    # Step 4: Validate required columns
    # -------------------------------
    required_columns = [
        "invoice_id",
        "customer_id",
        "product_id",
        "quantity",
        "total_amount",
        "transaction_date"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "CSV schema validation failed.",
                "missing_columns": missing_columns
            }
        )

    # -------------------------------
    # Step 5: Return success response
    # -------------------------------
    return {
        "status": "success",
        "message": "CSV uploaded and schema validated successfully.",
        "filename": file.filename,
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": dataframe.columns.tolist()
    }
