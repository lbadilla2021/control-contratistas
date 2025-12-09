from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.db import Company
from app.models.schemas import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", summary="List companies", response_model=list[CompanyRead])
async def list_companies(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(Company))
    return result.all()


@router.post(
    "/",
    summary="Create company",
    response_model=CompanyRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    company: CompanyCreate, session: AsyncSession = Depends(get_session)
):
    existing = await session.scalar(select(Company).where(Company.tax_id == company.tax_id))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with this tax ID already exists",
        )

    db_company = Company(**company.model_dump())
    session.add(db_company)
    await session.commit()
    await session.refresh(db_company)
    return db_company


@router.get("/{company_id}", summary="Get company", response_model=CompanyRead)
async def get_company(company_id: int, session: AsyncSession = Depends(get_session)):
    company = await session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@router.put("/{company_id}", summary="Update company", response_model=CompanyRead)
async def update_company(
    company_id: int, company_update: CompanyCreate, session: AsyncSession = Depends(get_session)
):
    company = await session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    conflict = await session.scalar(
        select(Company).where(Company.tax_id == company_update.tax_id, Company.id != company_id)
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with this tax ID already exists",
        )

    for field, value in company_update.model_dump().items():
        setattr(company, field, value)

    await session.commit()
    await session.refresh(company)
    return company


@router.delete("/{company_id}", summary="Delete company", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session)):
    company = await session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    await session.delete(company)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
