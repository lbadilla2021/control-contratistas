from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from app.core.config import settings


def create_access_token(subject: str, additional_claims: dict[str, Any] | None = None) -> str:
    to_encode: dict[str, Any] = {"sub": subject}
    if additional_claims:
        to_encode.update(additional_claims)

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_credentials(email: str, password: str) -> bool:
    return email.lower() == settings.admin_email.lower() and password == settings.admin_password
