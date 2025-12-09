import os
from datetime import datetime
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.core.storage import upload_object
from app.models.db import Document
from app.models.schemas import DocumentRead

router = APIRouter(prefix="/documentos", tags=["documents"])


@router.get("/", summary="List documents", response_model=list[DocumentRead])
async def list_documents(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Document))
    return result.all()


@router.post(
    "/",
    summary="Upload document",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    company_id: int = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    worker_id: int | None = Form(None),
    expires_at: datetime | None = Form(None),
    session: AsyncSession = Depends(get_session),
):
    allowed_types = {"application/pdf", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no permitido. Solo se aceptan PDF o JPG",
        )

    object_name = f"companies/{company_id}/{uuid4()}_{file.filename}"

    temp_file = NamedTemporaryFile(delete=False)
    try:
        content = await file.read()
        temp_file.write(content)
        temp_file.flush()

        upload_object(
            bucket_name=settings.minio_bucket,
            object_name=object_name,
            file_path=temp_file.name,
        )
    finally:
        temp_file.close()
        os.unlink(temp_file.name)

    document = Document(
        company_id=company_id,
        worker_id=worker_id,
        title=title,
        file_key=object_name,
        expires_at=expires_at,
    )
    session.add(document)
    await session.commit()
    await session.refresh(document)

    return document
