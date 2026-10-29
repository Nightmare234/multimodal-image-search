import uuid
from app.db.minio_client import minio_client, BUCKET_NAME
from app.config.config import settings

def upload_image(file_path: str) -> str:
    """Upload ảnh lên MinIO và trả về link public"""
    filename = f"{uuid.uuid4()}.jpg"
    minio_client.fput_object(BUCKET_NAME, filename, file_path)
    return f"{settings.MINIO_URI}/{BUCKET_NAME}/{file_name}"

