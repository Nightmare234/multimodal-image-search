
from pymilvus import Collection
from app.config.config import settings
from pymilvus import connections, Collection
# Kết nối Milvus trước
connections.connect("default", uri="http://localhost:19530")

# Mở collection
collection = Collection("search_image_to_image_collection")  # thay bằng tên collection bạn muốn

# In schema
print(collection.schema)

# # In số lượng entity
# print("Số lượng entities:", collection.num_entities)


# # Kết nối Milvus trước
# connections.connect("default", uri="http://localhost:19530")

# collection = Collection("search_image_to_image_collection")
# print("Số lượng entity trong collection:", collection.num_entities)