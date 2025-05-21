from fastapi import FastAPI, Request
from agent import query_agent, load_and_embed_pubmed

app = FastAPI()

@app.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    return {"response": query_agent(data["query"])}

@app.post("/load_pubmed")
async def load_pubmed(req: Request):
    data = await req.json()
    query = data.get("query", "")
    max_results = int(data.get("max_results", 10))
    load_and_embed_pubmed(query, max_results)
    return {"status": "PubMed articles loaded and embedded."}
