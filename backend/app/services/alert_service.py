from __future__ import annotations

import inspect
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from typing import Awaitable, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.db import Alert, Document, Expiration
from app.services.expiration_service import ExpirationStatus, verify_expirations

SendEmailCallable = Callable[[str, str, str], Awaitable[None] | None]


def _build_email(recipient: str, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from
    message["To"] = recipient
    message.set_content(body)
    return message


def send_email_alert(recipient: str, subject: str, body: str) -> None:
    message = _build_email(recipient, subject, body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_username:
            server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)


async def _dispatch_email(
    sender: SendEmailCallable, recipient: str, subject: str, body: str
) -> None:
    if inspect.iscoroutinefunction(sender):
        await sender(recipient, subject, body)
        return

    from asyncio import to_thread

    await to_thread(sender, recipient, subject, body)


async def send_document_alerts(
    session: AsyncSession,
    send_email: SendEmailCallable | None = None,
    warning_days: int = 30,
) -> dict[str, int]:
    """Send email alerts for expiring or expired documents.

    The function synchronizes expiration statuses, finds documents whose
    expirations are approaching or have passed, sends a single email per
    document, and records the attempt in the ``alerts`` table.
    """

    await verify_expirations(session, warning_days=warning_days)

    result = await session.scalars(
        select(Expiration)
        .where(Expiration.status.in_([ExpirationStatus.POR_VENCER, ExpirationStatus.VENCIDO]))
        .options(
            selectinload(Expiration.document)
            .selectinload(Document.worker),
            selectinload(Expiration.alerts),
        )
    )
    expirations = result.all()

    summary = {"alerts_sent": 0, "skipped": 0}
    sender = send_email or send_email_alert

    now = datetime.now(timezone.utc)

    for expiration in expirations:
        document = expiration.document
        worker = document.worker

        if worker is None or not worker.email:
            summary["skipped"] += 1
            continue

        already_sent = any(alert.channel == "email" for alert in expiration.alerts)
        if already_sent:
            summary["skipped"] += 1
            continue

        subject = f"Alerta de documento {expiration.status}"
        body = (
            f"El documento '{document.title}' vence el {expiration.expires_at.date()} "
            f"y se encuentra en estado: {expiration.status}."
        )

        await _dispatch_email(sender, worker.email, subject, body)

        alert = Alert(
            expiration_id=expiration.id,
            channel="email",
            sent_at=now,
        )
        session.add(alert)
        summary["alerts_sent"] += 1

    await session.commit()
    return summary


__all__ = ["send_document_alerts", "send_email_alert"]
