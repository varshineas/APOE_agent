from loader import load_pubmed_by_query
from embedder import embed
from llm import generate

store = VectorStore(dim=768)  # depending on your embedding size

def load_and_embed_pubmed(query: str, max_results=10):
    texts = load_pubmed_by_query(query, max_results)
    vectors = embed(texts).cpu().detach().numpy()
    store.add(vectors, texts)

def query_agent(user_query: str):
    qvec = embed([user_query]).cpu().detach().numpy()
    docs = store.search(qvec, k=5)
    prompt = f"Based on the following documents:\n\n{docs}\n\nAnswer the question:\n{user_query}"
    return generate(prompt)
