from pymilvus import MilvusClient
client = MilvusClient(uri="http://localhost:19530")
info = client.describe_collection("search_image_to_image_collection")
print(info)
