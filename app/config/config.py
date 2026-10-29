"""Centralized application settings loaded from environment variables or .env."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Milvus
    MILVUS_URI: str = "http://localhost:19530"
    COLLECTION_NAME_IMAGE: str = "search_image_to_image_collection"
    COLLECTION_NAME_TEXT: str = "images_clip_collection"
    VECTOR_DIM_IMAGE: int = 2048
    VECTOR_DIM_TEXT: int = 512
    MODEL_NAME_IMAGE: str = "resnet50"
    MODEL_NAME_TEXT: str = "ViT-B/32"

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_URI: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "images-upload-minio"

    # Local dataset path used by the ingestion scripts.
    IMAGE_DATA_DIR: str = "./data/images"


settings = Settings()
