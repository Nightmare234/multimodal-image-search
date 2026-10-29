import streamlit as st
import time
from PIL import Image
from app.services.embedding_images_service import generate_embedding
from app.search_image.search_img_to_img import get_milvus_client, get_search_results
from app.search_image.search_text_to_img import search_text
from pymilvus import Collection
from app.config.config import settings

# =========================
# Config Streamlit
# =========================
st.set_page_config(layout="wide")
st.title("Tìm kiếm ảnh")

# =========================
# Lấy config từ .env
# =========================
MILVUS_URI = settings.MILVUS_URI
COLLECTION_NAME_IMAGE = settings.COLLECTION_NAME_IMAGE
COLLECTION_NAME_TEXT = settings.COLLECTION_NAME_TEXT
OUTPUT_FIELDS = ["id", "file_name", "link", "type"]
MODEL_NAME_IMAGE = settings.MODEL_NAME_IMAGE
MINIO_BUCKET = settings.MINIO_BUCKET
MINIO_URI = settings.MINIO_URI
milvus_client = get_milvus_client(MILVUS_URI)

# =========================
# Sidebar chọn mode
# =========================
mode = st.sidebar.radio("Chọn chế độ tìm kiếm", ["Image → Image", "Text → Image"])
topk = st.sidebar.slider("Top K kết quả", 5, 50, 10, step=1)
show_distance = st.sidebar.toggle("Hiện điểm similarity")

# =========================
# Image → Image Search
# =========================
if mode == "Image → Image":
    uploaded_file = st.sidebar.file_uploader(
        "Upload ảnh query", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        query_img = Image.open(uploaded_file).convert("RGB")
        st.sidebar.image(query_img, caption="Query Image", width=200)

        query_vector = generate_embedding(query_img, MODEL_NAME_IMAGE)
        start = time.time()

        results = get_search_results(
            milvus_client=milvus_client,
            collection_name=COLLECTION_NAME_IMAGE,
            query_vector=query_vector,
            output_fields=OUTPUT_FIELDS,
            topk=topk,
        )

        elapsed = time.time() - start
        st.sidebar.write(f"⏱️ Thời gian tìm: {elapsed:.3f}s")

        formatted_results = []
        for hit in results[0]:
            row = hit.entity
            formatted_results.append(
                {
                    "file_name": row.get("file_name"),
                    "link": row.get("link"),
                    "score": hit.distance,
                }
            )

        cols = st.columns(5)
        for i, r in enumerate(formatted_results):
            with cols[i % 5]:
                if r["link"]:
                    st.image(r["link"], caption=r["file_name"], width='stretch')
                if show_distance:
                    st.caption(f"Score: {r['score']:.3f}")

# =========================
# Text → Image Search
# =========================
else:
    text_query = st.sidebar.text_area("Nhập mô tả ảnh bạn cần tìm", height=120)

    # 👉 Collection mặc định
    collection_option = "images_clip_collection"
    bucket_name="image-upload-minio"
    if st.sidebar.button("🔍 Tìm kiếm"):
        if text_query.strip():
            start = time.time()

            # ⚡ Tạo connection trước khi dùng Collection
            from pymilvus import connections, Collection
            connections.connect(alias="default", uri=MILVUS_URI)
            collection = Collection(name=collection_option, using="default")

            # Gọi search_text với collection trực tiếp
            results = search_text(
                text_query=text_query,
                collection=collection,
                topk=topk
            )

            elapsed = time.time() - start
            st.sidebar.write(f"⏱️ Thời gian tìm: {elapsed:.3f}s")

            if results:
                cols = st.columns(5)
                for i, r in enumerate(results):
                    # Chỉ dùng file_name từ MinIO để tạo URL public
                    if r.get("file_name"):
                        link = f"{MINIO_URI}/{MINIO_BUCKET}/{r['file_name']}"
                        with cols[i % 5]:
                            st.image(link, caption=r.get("file_name", ""), width='stretch')
                            if show_distance:
                                st.caption(f"Score: {r.get('score', 0):.3f}")
            else:
                st.info(
                    "❌ Không tìm thấy ảnh phù hợp. "
                    "Có thể collection chưa có embedding text hoặc embedding không tương thích."
                )
        else:
            st.sidebar.warning("⚠️ Vui lòng nhập mô tả trước khi tìm kiếm.")


