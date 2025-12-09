from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.db import Document, Expiration


class ExpirationStatus:
    VIGENTE = "vigente"
    POR_VENCER = "por_vencer"
    VENCIDO = "vencido"


def _determine_status(expires_at: datetime, now: datetime, warning_threshold: datetime) -> str:
    if expires_at < now:
        return ExpirationStatus.VENCIDO
    if expires_at <= warning_threshold:
        return ExpirationStatus.POR_VENCER
    return ExpirationStatus.VIGENTE


async def verify_expirations(session: AsyncSession, warning_days: int = 30) -> dict[str, int]:
    """Sync expiration statuses for documents.

    This function is intended to be executed by a scheduled job (e.g., daily)
    to ensure that every document with an expiration date has an associated
    Expiration row and that its status is updated according to the current
    date.
    """

    now = datetime.now(timezone.utc)
    warning_threshold = now + timedelta(days=warning_days)
    summary = {"processed": 0, "created": 0, "updated": 0}

    result = await session.scalars(
        select(Document)
        .where(Document.expires_at.is_not(None))
        .options(selectinload(Document.expiration))
    )
    documents = result.all()

    for document in documents:
        expires_at = document.expires_at
        if expires_at is None:
            continue

        status = _determine_status(expires_at, now, warning_threshold)
        expiration = document.expiration

        if expiration is None:
            session.add(
                Expiration(
                    document_id=document.id,
                    expires_at=expires_at,
                    status=status,
                )
            )
            summary["created"] += 1
        else:
            changes = False
            if expiration.expires_at != expires_at:
                expiration.expires_at = expires_at
                changes = True
            if expiration.status != status:
                expiration.status = status
                changes = True
            if changes:
                summary["updated"] += 1

        summary["processed"] += 1

    await session.commit()
    return summary


__all__ = ["ExpirationStatus", "verify_expirations"]
