from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.sales import router as sales_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.sales_transaction import (
    router as sales_transaction_router
)

app = FastAPI(
    title="MarketMind AI Backend"
)

# =====================================
# CORS Configuration
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# Register Routers
# =====================================

app.include_router(sales_router)
app.include_router(inventory_router)
app.include_router(sales_transaction_router)
