"""Create the ResNet50 image-to-image collection in Milvus.

Existing collections are preserved by default. Destructive recreation requires
an explicit --drop-existing flag.
"""
import argparse

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility,
)

from app.config.config import settings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="DANGER: delete the existing collection and all its data before recreating it.",
    )
    args = parser.parse_args()
    collection_name = settings.COLLECTION_NAME_IMAGE

    connections.connect(alias="default", uri=settings.MILVUS_URI)
    if utility.has_collection(collection_name):
        if not args.drop_existing:
            raise SystemExit(
                f"Collection '{collection_name}' already exists; it was not changed. "
                "Use --drop-existing only when you intentionally want to delete all its data."
            )
        print(f"WARNING: deleting collection '{collection_name}' and all its data.")
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="vector_image_embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.VECTOR_DIM_IMAGE),
        FieldSchema(name="image_description", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="phan_loai", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="short_title", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="hagtag_description", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="ngay_tao", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="ngay_sua", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="nguoi_tao", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="nguoi_sua", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="split", dtype=DataType.VARCHAR, max_length=50),
    ]
    schema = CollectionSchema(
        fields=fields,
        description="Collection chứa vector ResNet50 cho image-to-image search",
    )
    collection = Collection(name=collection_name, schema=schema)
    collection.create_index(
        field_name="vector_image_embedding",
        index_params={"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 1024}},
    )
    collection.load()
    print(f"Collection '{collection_name}' is ready.")


if __name__ == "__main__":
    main()
