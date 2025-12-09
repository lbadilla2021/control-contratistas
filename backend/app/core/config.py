from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ControlDoc API"
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/controldoc"
    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_email: str = "lbadilla1970@gmail.com"
    admin_password: str = "CerroColorado.2020"
    admin_full_name: str = "Administrador"
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    minio_bucket: str = "controldoc"
    minio_secure: bool = False
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from: str = "noreply@example.com"
    smtp_use_tls: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
