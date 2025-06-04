from fastapi import FastAPI

from backend.embeddings.qdrant_client import get_client
from backend.graph.nodes.llm_scoring import _ensure_collection

app = FastAPI(title="Trading Research Agent")


@app.on_event("startup")
async def _startup() -> None:
    client = get_client()
    await _ensure_collection(client)


@app.get("/health")
async def health():
    return {"status": "ok"}
