from pymilvus import connections, utility
from app.config.config import settings

def get_milvus_client(uri: str = settings.MILVUS_URI):
    """
    Kết nối tới Milvus và trả về connection client để thao tác (search, insert,...)
    """
    try:
        connections.connect(alias="default", uri=uri)
        print(f"✅ Đã kết nối tới Milvus tại {uri}")
        return connections.get_connection(alias="default")
    except Exception as e:
        print(f"❌ Kết nối Milvus thất bại: {e}")
        return None


def connect_milvus():
    """
    Hàm test đơn giản để kiểm tra kết nối Milvus.
    """
    try:
        connections.connect(alias="default", uri=settings.MILVUS_URI)
        version = utility.get_server_version()
        print(f"✅ Đã kết nối tới Milvus tại {settings.MILVUS_URI}")
        print(f"Milvus version: {version}")
        return True
    except Exception as e:
        print(f"❌ Kết nối Milvus thất bại: {e}")
        return False


if __name__ == "__main__":
    connect_milvus()
