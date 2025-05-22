from loader import load_pubmed_by_query
from embedder import embed
from vector_store import add, search, init_qdrant
from pubmed_utils import search_pubmed, fetch_best_available 
from paper_cache import is_pmid_loaded, mark_loaded
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
    docs = search(qvec, k=2)  # Adjust k as needed

    print("\n🔍 Retrieved documents from Qdrant:")
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Chunk {i} ---\n{doc[:500]}")

    context = "\n\n".join([doc[:400] for doc in docs])

    prompt = (
        f"You are a biomedical assistant. Use the following scientific excerpts to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {user_query}\n"
        f"Answer:"
    )

    print("\n🧠 Final prompt to LLaMA:\n" + prompt[:1000])
    return generate(prompt)


