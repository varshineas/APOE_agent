from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent import query_agent, load_and_embed_pubmed

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def preload():
    load_and_embed_pubmed("APOE Alzheimer", max_results=10)

@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def get_response(request: Request, user_input: str = Form(...)):
    response = query_agent(user_input)
    return templates.TemplateResponse("index.html", {"request": request, "response": response, "user_input": user_input})

@app.post("/load_pubmed")
async def api_load_pubmed(request: Request):
    data = await request.json()
    load_and_embed_pubmed(data.get("query", "APOE"), data.get("max_results", 5))
    return {"status": "PubMed papers loaded."}