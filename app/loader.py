from pubmed_utils import search_pubmed, fetch_best_available
from paper_cache import is_pmid_loaded, mark_loaded

def load_pubmed_by_query(query: str, max_results=10):
    pmids = search_pubmed(query, max_results)
    new_pmids, texts = [], []
    for pmid in pmids:
        if not is_pmid_loaded(pmid):
            text = fetch_best_available(pmid)
            if text.strip():
                texts.append(text)
                new_pmids.append(pmid)
                mark_loaded(pmid)
    return new_pmids, texts