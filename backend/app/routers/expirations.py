from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.db import Expiration
from app.models.schemas import ExpirationRead
from app.services.expiration_service import verify_expirations

router = APIRouter(prefix="/expirations", tags=["expirations"])


@router.get("/", summary="List expirations", response_model=list[ExpirationRead])
async def list_expirations(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Expiration))
    return result.all()


@router.post("/verify", summary="Run expiration verification")
async def run_verification(session: AsyncSession = Depends(get_session)):
    return await verify_expirations(session)
