from fastapi import APIRouter, Depends

from app.core.database import get_session

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", summary="List companies")
async def list_companies(session=Depends(get_session)):
    return {"detail": "not implemented"}
