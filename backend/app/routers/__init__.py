from fastapi import APIRouter

from app.routers import alerts, companies, documents, expirations, workers

api_router = APIRouter()
api_router.include_router(companies.router)
api_router.include_router(workers.router)
api_router.include_router(documents.router)
api_router.include_router(expirations.router)
api_router.include_router(alerts.router)

__all__ = ["api_router"]
