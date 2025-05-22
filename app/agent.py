from loader import load_pubmed_by_query
from embedder import embed
from vector_store import add, search, init_qdrant
from pubmed_utils import search_pubmed
from paper_cache import is_pmid_loaded
from llm import generate

init_qdrant()

def load_and_embed_pubmed(query: str, max_results=10):
    print(f"\nStarting PubMed preload for query: '{query}' (max {max_results})")
    
    pmids = search_pubmed(query, max_results)
    print(f"🔍 Retrieved {len(pmids)} PMIDs from PubMed")

    new_pmids, new_texts = [], []

    for pmid in pmids:
        if not is_pmid_loaded(pmid):
            text = fetch_best_available(pmid)
            if text.strip():
                new_pmids.append(pmid)
                new_texts.append(text)
                mark_loaded(pmid)
            else:
                print(f"Empty or invalid content for PMID {pmid}")
        else:
            print(f"⏩ Skipping already loaded PMID: {pmid}")

    print(f"📥 Found {len(new_texts)} new papers to embed")

    if not new_texts:
        print("No new content to embed. Skipping embedding.")
        return

    vectors = embed(new_texts).cpu().detach().numpy()
    add(vectors, new_texts, new_pmids)
    print(f"Embedded and indexed {len(new_texts)} new documents.\n")


def query_agent(user_query: str):
    qvec = embed([user_query]).cpu().detach().numpy()
    docs = search(qvec, k=5)
    prompt = f"Based on the following documents:\n\n{docs}\n\nAnswer the question:\n{user_query}"
    return generate(prompt)
