from loader import load_pubmed_by_query
from embedder import embed
from vector_store import add, search, init_qdrant
from pubmed_utils import search_pubmed
from paper_cache import is_pmid_loaded
from llm import generate

init_qdrant()

def load_and_embed_pubmed(query: str, max_results=10):
    pmids = search_pubmed(query, max_results)
    new_pmids, new_texts = [], []

    for pmid in pmids:
        if not is_pmid_loaded(pmid):
            text = load_pubmed_by_query(pmid, 1)[0]
            new_pmids.append(pmid)
            new_texts.append(text)

    if new_texts:
        vectors = embed(new_texts).cpu().detach().numpy()
        add(vectors, new_texts, new_pmids)

def query_agent(user_query: str):
    qvec = embed([user_query]).cpu().detach().numpy()
    docs = search(qvec, k=5)
    prompt = f"Based on the following documents:\n\n{docs}\n\nAnswer the question:\n{user_query}"
    return generate(prompt)
