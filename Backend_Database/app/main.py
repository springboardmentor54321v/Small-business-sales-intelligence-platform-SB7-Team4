from fastapi import FastAPI

from app.api.routes.sales import router as sales_router

app = FastAPI(
    title="MarketMind AI Backend"
)

app.include_router(sales_router)
