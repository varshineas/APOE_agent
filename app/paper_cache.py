loaded_pmids = set()

def is_pmid_loaded(pmid: str) -> bool:
    return pmid in loaded_pmids

def mark_loaded(pmid: str):
    loaded_pmids.add(pmid)