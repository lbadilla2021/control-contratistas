from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ControlDoc API"
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/controldoc"
    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    minio_bucket: str = "controldoc"
    minio_secure: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
