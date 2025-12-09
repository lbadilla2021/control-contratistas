from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.db import Company, Worker
from app.models.schemas import WorkerCreate, WorkerRead

router = APIRouter(prefix="/workers", tags=["workers"])


def _ensure_company_exists(company: Company | None):
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


@router.get("/", summary="List workers", response_model=list[WorkerRead])
async def list_workers(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Worker))
    return result.all()


@router.post(
    "/",
    summary="Create worker",
    response_model=WorkerRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_worker(
    worker: WorkerCreate, session: AsyncSession = Depends(get_session)
):
    company = await session.get(Company, worker.company_id)
    _ensure_company_exists(company)

    db_worker = Worker(**worker.model_dump())
    session.add(db_worker)
    await session.commit()
    await session.refresh(db_worker)
    return db_worker


@router.get("/{worker_id}", summary="Get worker", response_model=WorkerRead)
async def get_worker(worker_id: int, session: AsyncSession = Depends(get_session)):
    worker = await session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
    return worker


@router.put("/{worker_id}", summary="Update worker", response_model=WorkerRead)
async def update_worker(
    worker_id: int, worker_update: WorkerCreate, session: AsyncSession = Depends(get_session)
):
    worker = await session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    company = await session.get(Company, worker_update.company_id)
    _ensure_company_exists(company)

    for field, value in worker_update.model_dump().items():
        setattr(worker, field, value)

    await session.commit()
    await session.refresh(worker)
    return worker


@router.delete("/{worker_id}", summary="Delete worker", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(worker_id: int, session: AsyncSession = Depends(get_session)):
    worker = await session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    await session.delete(worker)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
