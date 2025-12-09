from fastapi import APIRouter, Depends

from app.core.database import get_session
from app.core.storage import upload_object

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/", summary="List documents")
async def list_documents(session=Depends(get_session)):
    return {"detail": "not implemented"}


@router.post("/upload", summary="Upload document placeholder")
async def upload_document(session=Depends(get_session)):
    return {"detail": "upload not implemented"}
