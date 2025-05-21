from Bio import Entrez

Entrez.email = "andy.varshine@gmail.com"  # Required by NCBI

def search_pubmed(query: str, max_results: int = 10) -> list[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]


def pubmed_to_pmc(pmid: str) -> str | None:
    handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
    record = Entrez.read(handle)
    try:
        pmcid = record[0]["LinkSetDb"][0]["Link"][0]["Id"]
        return f"PMC{pmcid}"
    except (IndexError, KeyError):
        return None


def fetch_abstract_from_pubmed(pmid: str) -> str:
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
        return handle.read()
    except Exception as e:
        return f"[ERROR fetching abstract for {pmid}]: {str(e)}"


def fetch_fulltext_from_pmc(pmcid: str) -> str:
    try:
        handle = Entrez.efetch(db="pmc", id=pmcid, rettype="full", retmode="text")
        return handle.read()
    except Exception as e:
        return f"[ERROR fetching full text for {pmcid}]: {str(e)}"


def fetch_best_available(pmid: str) -> str:
    pmcid = pubmed_to_pmc(pmid)
    if pmcid:
        fulltext = fetch_fulltext_from_pmc(pmcid)
        if "ERROR" not in fulltext:
            return fulltext
    return fetch_abstract_from_pubmed(pmid)
