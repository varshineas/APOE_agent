from fastapi import FastAPI, Request
from agent import query_agent

app = FastAPI()

@app.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    response = query_agent(data["query"])
    return {"response": response}
