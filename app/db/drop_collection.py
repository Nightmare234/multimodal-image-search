from pymilvus import connections, utility

# Kết nối Milvus
connections.connect("default", uri="http://localhost:19530")

# Tên collection muốn xóa
collection_name = "search_image_to_image_collection"

# Xóa collection
if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)
    print(f"✅ Đã xóa collection: {collection_name}")
else:
    print(f"⚠️ Collection {collection_name} không tồn tại")