from app.encoders.image_encoder import FeatureExtractor

def generate_embedding(image, model_name):
    encoder = FeatureExtractor(model_name)
    return encoder(image)
