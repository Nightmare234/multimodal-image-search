# app/services/embedding_text_service.py
from app.encoders.text_encoder import get_text_embedding, get_image_embedding
from PIL import Image


def generate_text_embedding(text: str):
    """
    Sinh embedding cho text (text → vector).
    Dùng cho chức năng tìm kiếm ảnh theo mô tả.
    """
    return get_text_embedding(text)


def generate_clip_image_embedding(image: Image.Image):
    """
    Sinh embedding cho ảnh bằng CLIP (image → vector).
    Dùng khi insert ảnh vào collection CLIP để phục vụ tìm kiếm text → image.
    """
    return get_image_embedding(image)
