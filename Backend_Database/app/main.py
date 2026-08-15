from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.sales import router as sales_router
from app.api.routes.customer import router as customer_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.sales_transaction import (
    router as sales_transaction_router
)
from app.api.routes.invoice import (
    router as invoice_router
)
from app.api.routes.payment import router as payment_router

from app.api.routes.revenue import (
    router as revenue_router
)

from app.api.routes.notification import router as notification_router

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
app.include_router(customer_router)
app.include_router(inventory_router)
app.include_router(sales_transaction_router)
app.include_router(invoice_router)
app.include_router(payment_router)
app.include_router(revenue_router)
app.include_router(notification_router)
