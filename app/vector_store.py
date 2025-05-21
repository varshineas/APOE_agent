import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, vectors, texts):
        self.index.add(vectors)
        self.texts.extend(texts)

    def search(self, query_vec, k=5):
        D, I = self.index.search(query_vec, k)
        return [self.texts[i] for i in I[0]]
