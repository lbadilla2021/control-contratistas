from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    workers: Mapped[list["Worker"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    documents: Mapped[list["Document"]] = relationship(back_populates="company", cascade="all, delete-orphan")


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped[Company] = relationship(back_populates="workers")
    documents: Mapped[list["Document"]] = relationship(back_populates="worker", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_key: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped[Company] = relationship(back_populates="documents")
    worker: Mapped[Worker | None] = relationship(back_populates="documents")
    expiration: Mapped["Expiration" | None] = relationship(back_populates="document", uselist=False, cascade="all, delete-orphan")


class Expiration(Base):
    __tablename__ = "expirations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    document: Mapped[Document] = relationship(back_populates="expiration")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="expiration", cascade="all, delete-orphan")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    expiration_id: Mapped[int] = mapped_column(ForeignKey("expirations.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False, default="email")
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    expiration: Mapped[Expiration] = relationship(back_populates="alerts")


__all__ = [
    "Base",
    "Company",
    "Worker",
    "Document",
    "Expiration",
    "Alert",
]
