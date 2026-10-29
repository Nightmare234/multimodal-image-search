import streamlit as st
from pymilvus import MilvusClient
from app.config.config import settings


# =========================
# Kết nối Milvus
# =========================
@st.cache_resource
def get_milvus_client(uri: str, token: str = None) -> MilvusClient:
    """
    Hàm này tạo kết nối với Milvus.
    Dùng cache để không tạo kết nối mới mỗi lần Streamlit rerun.
    """
    return MilvusClient(uri=uri, token=token)


# =========================
#  Tìm kiếm ảnh tương tự
# =========================
def get_search_results(milvus_client: MilvusClient, collection_name: str, query_vector, output_fields, topk=10):
    """
    Hàm này thực hiện tìm kiếm vector trong Milvus.
    """
    search_res = milvus_client.search(
        collection_name="search_image_to_image_collection",
        data=[query_vector],
        anns_field="vector_image_embedding",
        search_params={"metric_type": "COSINE", "params": {}},
        output_fields=["file_name", "link"],
        limit=10
    )

    return search_res


# =========================
# 4️⃣ Kiểm tra filename đã tồn tại chưa
# =========================
def search_by_filename(client, collection_name, filename):
    """
    Kiểm tra xem trong Milvus đã có vector nào gắn với filename này chưa.
    """
    try:
        from pymilvus import Collection

        collection = Collection(name=collection_name)
        results = collection.query(
            expr=f'file_name == "{filename}"',  # ✅ sửa tên field
            output_fields=["file_name"]         # ✅ sửa tên field
        )
        return results
    except Exception as e:
        print(f"Error searching filename {filename}: {e}")
        return []
