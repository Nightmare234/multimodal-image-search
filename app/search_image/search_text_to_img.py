from pymilvus import Collection
from app.encoders.text_encoder import get_text_embedding

def search_text(text_query: str, collection: Collection, topk: int = 10):
    """
    Tìm kiếm ảnh theo text query sử dụng CLIP embedding.
    """
    # ✅ Tạo embedding text bằng CLIP
    query_vector = get_text_embedding(text_query)

    # ✅ Thực hiện search trên Milvus
    results = collection.search(
        data=[query_vector],
        anns_field="vector_clip_embedding",  # phải đúng tên field trong schema
        param={"metric_type": "COSINE", "params": {"nprobe": 10}},
        limit=topk,
        output_fields=["file_name", "link", "title", "phan_loai"]
    )

    # ✅ Format kết quả
    output = []
    for hits in results:
        for hit in hits:
            row = hit.entity
            output.append({
                "file_name": row.get("file_name"),
                "link": row.get("link"),
                "score": hit.distance,
            })
    return output
