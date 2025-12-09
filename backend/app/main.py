from fastapi import FastAPI

from app.core.config import settings
from app.routers import api_router

app = FastAPI(title=settings.app_name)
app.include_router(api_router)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
