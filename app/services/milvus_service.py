from pymilvus import MilvusClient
from app.config.config import settings

# Khởi tạo 1 client toàn cục
milvus_client = MilvusClient(
    uri=settings.MILVUS_URI,
    token=settings.MILVUS_TOKEN if hasattr(settings, "MILVUS_TOKEN") else None
)

def get_milvus_client() -> MilvusClient:
    """
    Trả về client Milvus để các service khác dùng chung.
    """
    return milvus_client


def insert_embedding(entities: list):
    """
    Insert 1 batch entity vào Milvus.
    entities: list các dict có vector + metadata
    """
    client = get_milvus_client()

    try:
        res = client.insert(
            collection_name=settings.COLLECTION_NAME_TEXT,
            data=entities
        )
        print(f"✅ Inserted {len(entities)} embeddings vào Milvus")
        return res
    except Exception as e:
        print(f"❌ Lỗi insert vào Milvus: {e}")
        raise
