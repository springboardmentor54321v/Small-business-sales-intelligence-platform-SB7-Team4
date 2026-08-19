import pandas as pd
from fastapi import HTTPException


COLUMN_ALIASES = {
    "transaction_id": [
        "transaction_id",
        "transaction id",
    ],
    "order_id": [
        "order_id",
        "order id",
    ],
    "invoice_id": [
        "invoice_id",
        "invoice id",
        "invoice_no",
        "invoice no",
        "invoice number",
    ],
    "transaction_date": [
        "transaction_date",
        "transaction date",
        "order_date",
        "order date",
        "invoice_date",
        "invoice date",
        "date",
    ],
    "customer_id": [
        "customer_id",
        "customer id",
    ],
    "product_id": [
        "product_id",
        "product id",
    ],
    "quantity": [
        "quantity",
        "qty",
    ],
    "unit_price": [
        "unit_price",
        "unit price",
        "price",
    ],
    "discount": [
        "discount",
    ],
    "total_amount": [
        "total_amount",
        "total amount",
        "amount",
        "total",
        "sales",
        "sale",
        "revenue",
    ],
    "payment_method": [
        "payment_method",
        "payment method",
        "payment",
    ],
    "store_id": [
        "store_id",
        "store id",
    ],
    "created_by_user_id": [
        "created_by_user_id",
        "created by user id",
        "user_id",
    ],
    "city": [
        "city",
    ],
    "state": [
        "state",
    ],
    "country": [
        "country",
    ],
}


def normalize_column_name(column: str) -> str:
    return (
        str(column)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    return df


def find_column(df, aliases):
    normalized_aliases = {
        normalize_column_name(alias)
        for alias in aliases
    }

    for column in df.columns:
        if column in normalized_aliases:
            return column

    return None


def detect_and_map_columns(df: pd.DataFrame) -> pd.DataFrame:

    df = normalize_columns(df)

    mapping = {}

    for target, aliases in COLUMN_ALIASES.items():

        source = find_column(
            df,
            aliases
        )

        if source:
            mapping[source] = target

    df = df.rename(columns=mapping)

    # -------------------------------------------------
    # Required business fields
    # -------------------------------------------------

    required = [
        "customer_id",
        "product_id",
        "quantity",
        "total_amount",
        "transaction_date",
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unrecognized sales CSV format.",
                "missing_required_fields": missing,
                "supported_formats": [
                    "MarketMind cleaned sales dataset",
                    "MarketMind standardized sales CSV",
                    "Known sales CSV aliases",
                ],
            },
        )

    # -------------------------------------------------
    # Preserve Order ID when available
    # -------------------------------------------------

    if "order_id" in df.columns:

        df["order_id"] = (
            df["order_id"]
            .astype(str)
            .str.strip()
        )

    # -------------------------------------------------
    # Transaction ID
    # -------------------------------------------------

    if "transaction_id" not in df.columns:

        df["transaction_id"] = [
            f"UPL-TXN-{index:06d}"
            for index in range(
                1,
                len(df) + 1
            )
        ]

    # -------------------------------------------------
    # Invoice ID
    #
    # One invoice per Order ID.
    # -------------------------------------------------

    if "invoice_id" not in df.columns:

        if "order_id" in df.columns:

            df["invoice_id"] = (
                "UPL-INV-"
                + df["order_id"]
            )

        else:

            df["invoice_id"] = [
                f"UPL-INV-{index:06d}"
                for index in range(
                    1,
                    len(df) + 1
                )
            ]

    # -------------------------------------------------
    # Validate invoice ID length
    # -------------------------------------------------

    too_long_invoice_ids = df[
        df["invoice_id"].astype(str).str.len() > 30
    ]

    if not too_long_invoice_ids.empty:

        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "One or more invoice IDs exceed "
                    "the maximum length of 30 characters."
            },
        )

    # -------------------------------------------------
    # Transaction date
    # -------------------------------------------------

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    ).dt.date

    # -------------------------------------------------
    # Numeric fields
    # -------------------------------------------------

    for column in [
        "quantity",
        "unit_price",
        "discount",
        "total_amount",
    ]:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # -------------------------------------------------
    # Defaults
    # -------------------------------------------------

    if "discount" not in df.columns:
        df["discount"] = 0

    if "unit_price" not in df.columns:

        df["unit_price"] = (
            df["total_amount"]
            / df["quantity"].replace(0, pd.NA)
        )

    if "payment_method" not in df.columns:
        df["payment_method"] = "Unknown"

    if "created_by_user_id" not in df.columns:
        df["created_by_user_id"] = 1

    # -------------------------------------------------
    # Remove all-null and exact duplicate rows
    # -------------------------------------------------

    df = (
        df
        .dropna(how="all")
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # -------------------------------------------------
    # Validate values & filter invalid rows
    # -------------------------------------------------

    for col in ["customer_id", "product_id"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    invalid_mask = (
        df["transaction_date"].isna()
        | df["customer_id"].isna()
        | df["product_id"].isna()
        | df["quantity"].isna()
        | (df["quantity"] <= 0)
        | df["total_amount"].isna()
        | (df["total_amount"] < 0)
    )

    valid_df = df[~invalid_mask].copy().reset_index(drop=True)

    if valid_df.empty:

        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "Sales CSV contains no valid data rows.",
                "invalid_row_count":
                    len(df),
            },
        )

    return valid_df
