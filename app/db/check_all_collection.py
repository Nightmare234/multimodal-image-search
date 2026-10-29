from pymilvus import connections, utility

# Kết nối Milvus
connections.connect("default", uri="http://localhost:19530")

# # Liệt kê tất cả collections
# print(utility.list_collections())

from pymilvus import Collection
col = Collection("search_image_to_image_collection")
print("✅ Tổng số bản ghi:", col.num_entities)
