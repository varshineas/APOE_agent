from sentence_transformers import SentenceTransformer
model = SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')
def embed(texts: list[str]):
    return model.encode(texts, convert_to_tensor=True)
