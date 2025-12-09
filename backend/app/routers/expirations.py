from fastapi import APIRouter, Depends

from app.core.database import get_session

router = APIRouter(prefix="/expirations", tags=["expirations"])


@router.get("/", summary="List expirations")
async def list_expirations(session=Depends(get_session)):
    return {"detail": "not implemented"}
