from fastapi import FastAPI
from app.orchestrator import Orchestrator
from app.schemas.request import UserRequest, ChatResponse

app = FastAPI(title="Ecommerce Multi-Agent System", version="1.0.0")
orchestrator = Orchestrator()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: UserRequest):
    result = await orchestrator.handle(req)
    return result
