from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.db import Company, Worker
from app.models.schemas import WorkerCreate, WorkerRead

router = APIRouter(prefix="/workers", tags=["workers"])


@router.get("/", response_model=list[WorkerRead], summary="List workers")
async def list_workers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Worker))
    return result.scalars().all()


@router.post(
    "/",
    response_model=WorkerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create worker",
)
async def create_worker(
    payload: WorkerCreate, session: AsyncSession = Depends(get_session)
):
    company = await session.get(Company, payload.company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    worker = Worker(**payload.model_dump())
    session.add(worker)
    await session.commit()
    await session.refresh(worker)
    return worker


@router.get("/{worker_id}", response_model=WorkerRead, summary="Get worker")
async def get_worker(worker_id: int, session: AsyncSession = Depends(get_session)):
    worker = await session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return worker


@router.put("/{worker_id}", response_model=WorkerRead, summary="Update worker")
async def update_worker(
    worker_id: int, payload: WorkerCreate, session: AsyncSession = Depends(get_session)
):
    worker = await session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    company = await session.get(Company, payload.company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    for field, value in payload.model_dump().items():
        setattr(worker, field, value)

    await session.commit()
    await session.refresh(worker)
    return worker


@router.delete("/{worker_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete worker")
async def delete_worker(worker_id: int, session: AsyncSession = Depends(get_session)):
    worker = await session.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    await session.delete(worker)
    await session.commit()
