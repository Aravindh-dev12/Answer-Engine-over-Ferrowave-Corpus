import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = Path(os.getenv("CORPUS_DIR", BASE_DIR / "corpus"))
INDEX_CACHE_DIR = Path(os.getenv("INDEX_CACHE_DIR", BASE_DIR / ".index_cache"))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# Cost rates per 1,000,000 tokens (USD)
# Gemini 2.5 Flash: $0.075 / 1M prompt, $0.30 / 1M completion
# GPT-4o-mini: $0.15 / 1M prompt, $0.60 / 1M completion
# Claude 3.5 Haiku: $0.80 / 1M prompt, $4.00 / 1M completion
MODEL_COSTS = {
    "gemini-2.5-flash": {"in": 0.075 / 1_000_000, "out": 0.30 / 1_000_000},
    "gemini-1.5-flash": {"in": 0.075 / 1_000_000, "out": 0.30 / 1_000_000},
    "gpt-4o-mini": {"in": 0.15 / 1_000_000, "out": 0.60 / 1_000_000},
    "gpt-4o": {"in": 2.50 / 1_000_000, "out": 10.00 / 1_000_000},
    "claude-3-5-haiku-20241022": {"in": 0.80 / 1_000_000, "out": 4.00 / 1_000_000},
    "mock": {"in": 0.0, "out": 0.0}
}

def get_model_cost(model_name: str, tokens_in: int, tokens_out: int) -> float:
    rates = MODEL_COSTS.get(model_name, {"in": 0.10 / 1_000_000, "out": 0.40 / 1_000_000})
    return round((tokens_in * rates["in"]) + (tokens_out * rates["out"]), 6)
