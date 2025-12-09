from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.models.db import Alert, Company, Document, Expiration, Worker
from app.services.alert_service import send_document_alerts
from app.services.expiration_service import ExpirationStatus


@pytest.mark.asyncio
async def test_send_document_alerts_sends_for_expiring_and_expired(db_session):
    now = datetime.now(timezone.utc)
    company = Company(name="Alert Corp", tax_id="AL123", compliance_expires_at=now)
    worker = Worker(
        company_id=1,
        first_name="Ana",
        last_name="Perez",
        email="ana@example.com",
        certification_expires_at=None,
    )
    db_session.add(company)
    await db_session.flush()

    worker.company_id = company.id
    db_session.add(worker)
    await db_session.flush()

    documents = [
        Document(
            company_id=company.id,
            worker_id=worker.id,
            title="Seguro",
            file_key="insurance.pdf",
            expires_at=now + timedelta(days=5),
        ),
        Document(
            company_id=company.id,
            worker_id=worker.id,
            title="Contrato",
            file_key="contract.pdf",
            expires_at=now - timedelta(days=1),
        ),
        Document(
            company_id=company.id,
            worker_id=worker.id,
            title="Guia",
            file_key="guide.pdf",
            expires_at=now + timedelta(days=60),
        ),
        Document(
            company_id=company.id,
            worker_id=None,
            title="Sin responsable",
            file_key="no-worker.pdf",
            expires_at=now - timedelta(days=2),
        ),
    ]

    db_session.add_all(documents)
    await db_session.flush()

    expirations = [
        Expiration(
            document_id=documents[0].id,
            expires_at=documents[0].expires_at,
            status=ExpirationStatus.POR_VENCER,
        ),
        Expiration(
            document_id=documents[1].id,
            expires_at=documents[1].expires_at,
            status=ExpirationStatus.VENCIDO,
        ),
        Expiration(
            document_id=documents[2].id,
            expires_at=documents[2].expires_at,
            status=ExpirationStatus.VIGENTE,
        ),
        Expiration(
            document_id=documents[3].id,
            expires_at=documents[3].expires_at,
            status=ExpirationStatus.VENCIDO,
        ),
    ]
    db_session.add_all(expirations)
    await db_session.commit()

    sent_messages: list[tuple[str, str, str]] = []

    async def fake_send(recipient: str, subject: str, body: str):
        sent_messages.append((recipient, subject, body))

    summary = await send_document_alerts(db_session, send_email=fake_send)

    assert summary == {"alerts_sent": 2, "skipped": 2}
    assert len(sent_messages) == 2
    assert all("Ana" not in subject for _, subject, _ in sent_messages)

    result = await db_session.scalars(select(Alert).order_by(Alert.expiration_id))
    alerts = result.all()
    assert len(alerts) == 2
    assert all(alert.channel == "email" and alert.sent_at is not None for alert in alerts)


@pytest.mark.asyncio
async def test_send_document_alerts_skips_existing_alerts(db_session):
    now = datetime.now(timezone.utc)
    company = Company(name="Repeat", tax_id="REP123", compliance_expires_at=now)
    worker = Worker(
        company_id=1,
        first_name="Luis",
        last_name="Lopez",
        email="luis@example.com",
        certification_expires_at=None,
    )
    db_session.add(company)
    await db_session.flush()

    worker.company_id = company.id
    db_session.add(worker)
    await db_session.flush()

    document = Document(
        company_id=company.id,
        worker_id=worker.id,
        title="Licencia",
        file_key="license.pdf",
        expires_at=now - timedelta(days=3),
    )
    db_session.add(document)
    await db_session.flush()

    expiration = Expiration(
        document_id=document.id,
        expires_at=document.expires_at,
        status=ExpirationStatus.VENCIDO,
    )
    db_session.add(expiration)
    await db_session.flush()

    alert = Alert(expiration_id=expiration.id, channel="email", sent_at=now)
    db_session.add(alert)
    await db_session.commit()

    summary = await send_document_alerts(db_session, send_email=lambda *args, **kwargs: None)

    assert summary == {"alerts_sent": 0, "skipped": 1}

    result = await db_session.scalars(select(Alert))
    alerts = result.all()
    assert len(alerts) == 1
