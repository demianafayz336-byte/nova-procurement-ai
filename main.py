from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from agent_logic import run_procurement

load_dotenv()

app = FastAPI(title="Multi-Agent Procurement Assistant")

if not os.path.exists("templates"):
    os.makedirs("templates")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/procure", response_class=HTMLResponse)
async def procure(request: Request, query: str = Form(...)):
    print(f"🚀 Starting procurement for: {query}")
    result = await run_procurement(query)
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "query": query})