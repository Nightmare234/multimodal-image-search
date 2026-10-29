from pymilvus import MilvusClient

client = MilvusClient(uri="http://localhost:19530")

info = client.describe_collection("images_clip_collection")
print("\n=== SCHEMA INFO ===")
for field in info["fields"]:
    print(f"- {field['name']} ({field['type']})")
