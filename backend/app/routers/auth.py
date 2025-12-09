from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, verify_credentials
from app.models.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    if not verify_credentials(payload.email, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token = create_access_token(
        subject=payload.email,
        additional_claims={"name": settings.admin_full_name},
    )
    return TokenResponse(access_token=token, token_type="bearer")
