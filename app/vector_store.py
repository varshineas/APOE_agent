from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, SearchRequest
from uuid import uuid4
import os
import numpy as np

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "apoe_chunks"
CHUNK_SIZE = 500  # max ~500 characters per chunk

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_qdrant():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

init_qdrant()

def chunk_text(text: str, max_len: int = CHUNK_SIZE):
    sentences = text.split('. ')
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_len:
            current += sentence + '. '
        else:
            chunks.append(current.strip())
            current = sentence + '. '
    if current:
        chunks.append(current.strip())
    return chunks

def add(vectors, texts, ids):
    points = []
    for text, vector, pmid in zip(texts, vectors, ids):
        vector = np.array(vector, dtype=np.float32)  # Ensure correct dtype
        chunks = chunk_text(text)
        for chunk in chunks:
            points.append(PointStruct(
                id=str(uuid4()),
                vector=vector.tolist(),
                payload={"text": chunk, "pmid": pmid}
            ))
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search(vector, k=3):
    vector = np.array(vector, dtype=np.float32).flatten().tolist()  # Ensure float32 and flat list
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=k
    )
    return [hit.payload["text"] for hit in hits]
