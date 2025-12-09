from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.db import Alert
from app.models.schemas import AlertRead
from app.services.alert_service import send_document_alerts

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", summary="List alerts", response_model=list[AlertRead])
async def list_alerts(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Alert))
    return result.all()


@router.post("/send", summary="Send email alerts")
async def send_alerts(session: AsyncSession = Depends(get_session)):
    return await send_document_alerts(session)
