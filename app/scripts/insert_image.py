"""Insert image embeddings (ResNet50) from a local dataset into MinIO and Milvus.

Usage: python -m app.scripts.insert_image --data-dir ./data/images
or set IMAGE_DATA_DIR in the environment / .env file.
"""
import argparse
import io
import os
from pathlib import Path

from minio import Minio
from PIL import Image
from pymilvus import Collection, connections

from app.config.config import settings
from app.scripts.dataset_utils import resolve_dataset_dir
from app.services.embedding_images_service import FeatureExtractor


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Insert image vectors into Milvus.")
    parser.add_argument(
        "--data-dir",
        default=os.getenv("IMAGE_DATA_DIR", settings.IMAGE_DATA_DIR),
        help="Folder containing source images (default: IMAGE_DATA_DIR or ./data/images).",
    )
    return parser.parse_args()


def main() -> None:
    data_dir = resolve_dataset_dir(parse_args().data_dir)
    if not data_dir.is_dir():
        raise SystemExit(
            f"Dataset folder not found: {data_dir}\n"
            "Create the folder, add images you are authorized to use, or pass --data-dir."
        )

    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_URI.startswith("https://"),
    )
    if not minio_client.bucket_exists(settings.MINIO_BUCKET):
        raise SystemExit(
            f"MinIO bucket '{settings.MINIO_BUCKET}' does not exist. Create it first."
        )

    connections.connect(alias="default", uri=settings.MILVUS_URI)
    collection = Collection(settings.COLLECTION_NAME_IMAGE)
    collection.load()
    image_encoder = FeatureExtractor(settings.MODEL_NAME_IMAGE)

    inserted = 0
    for file_path in data_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        try:
            file_name = file_path.name
            minio_client.fput_object(settings.MINIO_BUCKET, file_name, str(file_path))
            image_url = f"{settings.MINIO_URI.rstrip('/')}/{settings.MINIO_BUCKET}/{file_name}"
            with file_path.open("rb") as image_file:
                image = Image.open(io.BytesIO(image_file.read())).convert("RGB")
                vector = image_encoder(image)

            entity = {
                "file_name": file_name,
                "title": file_name,
                "link": image_url,
                "vector_image_embedding": vector,
                "image_description": "",
                "phan_loai": "",
                "short_title": "",
                "name": "",
                "hagtag_description": "",
                "ngay_tao": "",
                "ngay_sua": "",
                "nguoi_tao": "",
                "nguoi_sua": "",
                "split": "",
            }
            collection.insert([entity])
            inserted += 1
            print(f"Inserted: {file_name}")
        except Exception as exc:
            print(f"Skipped '{file_path.name}': {exc}")

    collection.flush()
    print(f"Finished. Inserted {inserted} image(s).")


if __name__ == "__main__":
    main()
