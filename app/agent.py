from embedder import embed
from vector_store import VectorStore
from llm import generate

store = VectorStore(dim=768)  # depending on your embedding size

def query_agent(query):
    qvec = embed([query]).cpu().detach().numpy()
    relevant_docs = store.search(qvec, k=5)
    prompt = f"Answer this question based on these documents:\n\n{relevant_docs}\n\nQ: {query}"
    return generate(prompt)
