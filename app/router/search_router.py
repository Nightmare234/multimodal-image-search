from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io, time

from pymilvus import connections, Collection

from app.services.embedding_images_service import generate_embedding
from app.search_image.search_img_to_img import get_milvus_client, get_search_results
from app.search_image.search_text_to_img import search_text
from app.config.config import settings
from app.services.embedding_text_service import generate_text_embedding

router = APIRouter(prefix="/search", tags=["Search"])

# =========================
# Config
# =========================
MILVUS_URI = settings.MILVUS_URI
COLLECTION_NAME_IMAGE = "search_image_to_image_collection"
COLLECTION_NAME_TEXT = "images_clip_collection"
OUTPUT_FIELDS = ["id", "file_name", "link", "type"]
MODEL_NAME = settings.MODEL_NAME_IMAGE
MODEL_NAME_TEXT = settings.MODEL_NAME_TEXT
MINIO_URI = settings.MINIO_URI
MINIO_BUCKET = "image-upload-minio"

milvus_client = get_milvus_client(MILVUS_URI)


@router.post("/image")
async def search_by_image(file: UploadFile = File(...), topk: int = 10):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        query_vector = generate_embedding(image, MODEL_NAME)

        # Đảm bảo query_vector dạng list cho Milvus
        if isinstance(query_vector[0], float):
            query_vector = [query_vector]

        start = time.time()
        results = get_search_results(
            milvus_client=milvus_client,
            collection_name=COLLECTION_NAME_IMAGE,
            query_vector=query_vector,
            output_fields=OUTPUT_FIELDS,
            topk=topk,
        )
        elapsed = time.time() - start

        formatted_results = []
        for hit in results[0]:
            row = hit.entity
            link = row.get("link") or f"{MINIO_URI}/{MINIO_BUCKET}/{row.get('file_name')}"
            formatted_results.append({
                "file_name": row.get("file_name"),
                "link": link,
                "score": hit.distance
            })

        return JSONResponse({"elapsed": round(elapsed, 3), "results": formatted_results})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



# =========================
# Text → Image Search API
# =========================
@router.post("/text")
async def search_by_text(
    text_query: str = Form(...),
    topk: int = Form(10)
):
    """
    API: Tìm kiếm ảnh bằng text (Text → Image Search)
    """
    try:
        if not text_query.strip():
            return JSONResponse(status_code=400, content={"error": "Empty query"})

        start = time.time()

        # 1️⃣ Kết nối Milvus
        connections.connect(alias="default", uri=MILVUS_URI)
        collection = Collection(name=COLLECTION_NAME_TEXT, using="default")

        # 2️⃣ Gọi search_text() (không có milvus_client)
        results = search_text(
            text_query=text_query,
            collection=collection,
            topk=topk
        )

        elapsed = time.time() - start

        # 3️⃣ Format kết quả
        formatted_results = []
        for r in results:
            link = r.get("link")
            # Nếu link chưa có dạng URL thì tạo từ MinIO
            if not link and r.get("file_name"):
                link = f"{MINIO_URI}/{MINIO_BUCKET}/{r['file_name']}"

            formatted_results.append({
                "file_name": r.get("file_name"),
                "link": link,
                "score": r.get("score")
            })

        return JSONResponse({
            "elapsed_time": round(elapsed, 3),
            "results": formatted_results
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})