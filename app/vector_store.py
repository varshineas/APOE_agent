from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid
import numpy as np

COLLECTION_NAME = "apoe-papers"

client = QdrantClient(host="qdrant", port=6333)

# Initialize collection if not exists
def init_qdrant(dim=768):
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

def add(vectors, texts, pmids):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec.tolist(),
            payload={"text": text, "pmid": pmid}
        )
        for vec, text, pmid in zip(vectors, texts, pmids)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search(query_vector, k=5):
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector[0].tolist(),
        limit=k
    )
    return [hit.payload["text"] for hit in hits]

def is_pmid_loaded(pmid):
    result = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1,
        filter=Filter(
            must=[
                FieldCondition(key="pmid", match=MatchValue(value=pmid))
            ]
        )
    )
    return len(result[0]) > 0
