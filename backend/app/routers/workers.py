from fastapi import APIRouter, Depends

from app.core.database import get_session

router = APIRouter(prefix="/workers", tags=["workers"])


@router.get("/", summary="List workers")
async def list_workers(session=Depends(get_session)):
    return {"detail": "not implemented"}
