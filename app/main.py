import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from app.config import CORPUS_DIR, INDEX_CACHE_DIR, MODEL_NAME
from app.models import AskRequest, AskResponse, HealthResponse
from app.indexer import CorpusIndex
from app.engine import AnswerEngine

index = CorpusIndex()
engine: AnswerEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global index, engine
    manifest_path = CORPUS_DIR / "_manifest.csv"
    if (INDEX_CACHE_DIR / "index_data.json").exists() and (INDEX_CACHE_DIR / "bm25.pkl").exists():
        index = CorpusIndex.load(INDEX_CACHE_DIR, manifest_path)
    else:
        index.build_from_corpus(CORPUS_DIR, manifest_path)
        index.save(INDEX_CACHE_DIR)
    engine = AnswerEngine(index)
    yield

app = FastAPI(title="Ferrowave Pulse Answer Engine", lifespan=lifespan)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        ok=True,
        documents_indexed=len(index.raw_documents),
        model=MODEL_NAME
    )

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    if engine is None:
        raise HTTPException(status_code=503, detail="Answer engine is not initialized.")
    return await engine.ask(request.question)
