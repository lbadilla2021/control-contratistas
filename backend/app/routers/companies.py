from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.db import Company
from app.models.schemas import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[CompanyRead], summary="List companies")
async def list_companies(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Company))
    return result.scalars().all()


@router.post(
    "/",
    response_model=CompanyRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create company",
)
async def create_company(
    payload: CompanyCreate, session: AsyncSession = Depends(get_session)
):
    company = Company(**payload.model_dump())
    session.add(company)
    await session.commit()
    await session.refresh(company)
    return company


@router.get("/{company_id}", response_model=CompanyRead, summary="Get company")
async def get_company(company_id: int, session: AsyncSession = Depends(get_session)):
    company = await session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return company


@router.put("/{company_id}", response_model=CompanyRead, summary="Update company")
async def update_company(
    company_id: int,
    payload: CompanyCreate,
    session: AsyncSession = Depends(get_session),
):
    company = await session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    for field, value in payload.model_dump().items():
        setattr(company, field, value)

    await session.commit()
    await session.refresh(company)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete company")
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session)):
    company = await session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    await session.delete(company)
    await session.commit()
