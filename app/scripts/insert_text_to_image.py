"""Insert CLIP image embeddings from a local dataset into MinIO and Milvus.

Usage: python -m app.scripts.insert_text_to_image --data-dir ./data/images
or set IMAGE_DATA_DIR in the environment / .env file.
"""
import argparse
import os
from pathlib import Path

from minio import Minio
from PIL import Image
from pymilvus import Collection, connections

from app.config.config import settings
from app.scripts.dataset_utils import resolve_dataset_dir
from app.encoders.text_encoder import get_image_embedding


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Insert CLIP image vectors into Milvus.")
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
        minio_client.make_bucket(settings.MINIO_BUCKET)

    connections.connect(alias="default", uri=settings.MILVUS_URI)
    collection = Collection(settings.COLLECTION_NAME_TEXT)
    collection.load()

    inserted = 0
    for file_path in data_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        try:
            file_name = file_path.name
            category = file_path.parent.name
            text_description = f"{category} {file_path.stem}".strip()
            with file_path.open("rb") as image_file:
                minio_client.put_object(
                    settings.MINIO_BUCKET,
                    file_name,
                    data=image_file,
                    length=file_path.stat().st_size,
                    content_type="image/jpeg" if file_path.suffix.lower() in {".jpg", ".jpeg"} else "application/octet-stream",
                )
            image = Image.open(file_path).convert("RGB")
            vector_image = get_image_embedding(image)
            link_minio = f"{settings.MINIO_URI.rstrip('/')}/{settings.MINIO_BUCKET}/{file_name}"
            entities = [
                [file_name], [text_description], [link_minio], [vector_image],
                [text_description], [category], [text_description], [text_description],
                ["#hashtag_demo"], [""], [""], [""], [""], ["train"],
            ]
            collection.insert(entities)
            inserted += 1
            print(f"Inserted: {file_name} (category: {category})")
        except Exception as exc:
            print(f"Skipped '{file_path.name}': {exc}")

    collection.flush()
    print(f"Finished. Inserted {inserted} image(s).")


if __name__ == "__main__":
    main()
