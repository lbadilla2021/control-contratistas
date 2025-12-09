from minio import Minio

from app.core.config import settings


client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)


def ensure_bucket_exists(bucket_name: str) -> None:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


def upload_object(bucket_name: str, object_name: str, file_path: str) -> None:
    ensure_bucket_exists(bucket_name)
    client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)
