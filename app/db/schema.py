from pymilvus import FieldSchema, CollectionSchema, DataType

# Định nghĩa các field
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector_image_embedding", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="image_description", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="short_title", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="hagtag_description", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="created_at", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="updated_at", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="created_by", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="updated_by", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
]

# Định nghĩa schema nhưng KHÔNG tạo collection
schema = CollectionSchema(fields=fields, description="Schema lưu trữ metadata và embedding ảnh")
