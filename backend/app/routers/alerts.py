from fastapi import APIRouter, Depends

from app.core.database import get_session

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", summary="List alerts")
async def list_alerts(session=Depends(get_session)):
    return {"detail": "not implemented"}
