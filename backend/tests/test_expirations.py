from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.models.db import Company, Document, Expiration
from app.services.expiration_service import ExpirationStatus, verify_expirations


@pytest.mark.asyncio
async def test_verify_expirations_sets_statuses(db_session):
    now = datetime.now(timezone.utc)
    company = Company(name="Status Co", tax_id="ST123", compliance_expires_at=now)
    db_session.add(company)
    await db_session.flush()

    documents = [
        Document(
            company_id=company.id,
            worker_id=None,
            title="Contrato largo",
            file_key="contract.pdf",
            expires_at=now + timedelta(days=40),
        ),
        Document(
            company_id=company.id,
            worker_id=None,
            title="Seguro pronto",
            file_key="insurance.pdf",
            expires_at=now + timedelta(days=5),
        ),
        Document(
            company_id=company.id,
            worker_id=None,
            title="Licencia vencida",
            file_key="license.pdf",
            expires_at=now - timedelta(days=1),
        ),
    ]
    db_session.add_all(documents)
    await db_session.commit()

    summary = await verify_expirations(db_session, warning_days=10)

    assert summary == {"processed": 3, "created": 3, "updated": 0}

    result = await db_session.scalars(select(Expiration).order_by(Expiration.document_id))
    expirations = result.all()
    statuses = [expiration.status for expiration in expirations]
    assert statuses == [
        ExpirationStatus.VIGENTE,
        ExpirationStatus.POR_VENCER,
        ExpirationStatus.VENCIDO,
    ]


@pytest.mark.asyncio
async def test_verify_updates_existing_expiration(db_session):
    now = datetime.now(timezone.utc)
    company = Company(name="Updater", tax_id="UPD123", compliance_expires_at=now)
    db_session.add(company)
    await db_session.flush()

    document = Document(
        company_id=company.id,
        worker_id=None,
        title="Doc a actualizar",
        file_key="update.pdf",
        expires_at=now + timedelta(days=2),
    )
    db_session.add(document)
    await db_session.flush()

    expiration = Expiration(
        document_id=document.id,
        expires_at=document.expires_at,
        status=ExpirationStatus.VIGENTE,
    )
    db_session.add(expiration)
    await db_session.commit()

    document.expires_at = now - timedelta(days=1)
    await db_session.commit()

    summary = await verify_expirations(db_session, warning_days=5)
    assert summary["updated"] == 1

    refreshed = await db_session.scalar(
        select(Expiration).where(Expiration.document_id == document.id)
    )
    assert refreshed.status == ExpirationStatus.VENCIDO
    assert refreshed.expires_at == document.expires_at
