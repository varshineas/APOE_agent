from pubmed_utils import search_pubmed, fetch_best_available
import fitz  # PyMuPDF

def load_pdf(filepath):
    doc = fitz.open(filepath)
    return "\n".join([page.get_text() for page in doc])

def load_pubmed_by_query(query: str, max_results=10) -> list[str]:
    pmids = search_pubmed(query, max_results)
    return [fetch_best_available(pmid) for pmid in pmids]