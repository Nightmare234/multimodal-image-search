from minio import Minio
from app.config.config import settings

BUCKET_NAME = settings.MINIO_BUCKET  # hoặc tên bucket bạn muốn mặc định

# Tạo client toàn cục để import dùng luôn
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def connect_minio():
    try:
        buckets = minio_client.list_buckets()
        if buckets:
            print("✅ Đã kết nối thành công tới MinIO")
            print("Danh sách bucket có trong MinIO:")
            for bucket in buckets:
                print(f" - {bucket.name}")
        else:
            print("✅ Đã kết nối tới MinIO (nhưng chưa có bucket nào).")

        return True
    except Exception as e:
        print(f"❌ Kết nối MinIO thất bại: {e}")
        return False


if __name__ == "__main__":
    connect_minio()
