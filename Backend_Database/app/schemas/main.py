from fastapi import FastAPI

from app.api.routes.sales import router as sales_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.sales_transaction import (
    router as sales_transaction_router
)

app = FastAPI(
    title="MarketMind AI Backend"
)

app.include_router(sales_router)

app.include_router(inventory_router)

app.include_router(sales_transaction_router)
