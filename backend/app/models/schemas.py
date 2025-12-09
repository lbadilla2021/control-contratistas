from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CompanyBase(BaseModel):
    name: str
    tax_id: str
    compliance_expires_at: datetime | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WorkerBase(BaseModel):
    company_id: int
    first_name: str
    last_name: str
    email: EmailStr
    certification_expires_at: datetime | None = None


class WorkerCreate(WorkerBase):
    pass


class WorkerRead(WorkerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    company_id: int
    worker_id: Optional[int]
    title: str
    file_key: str
    expires_at: datetime | None = None


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExpirationBase(BaseModel):
    document_id: int
    expires_at: datetime
    status: str


class ExpirationCreate(ExpirationBase):
    pass


class ExpirationRead(ExpirationBase):
    id: int

    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    expiration_id: int
    channel: str = "email"
    sent_at: Optional[datetime] = None


class AlertCreate(AlertBase):
    pass


class AlertRead(AlertBase):
    id: int

    class Config:
        from_attributes = True
