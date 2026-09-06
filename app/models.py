from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Citation(BaseModel):
    path: str = Field(description="Relative path of file in corpus, e.g. policies/refund-policy.md")
    quote: str = Field(description="Verbatim text from the file, max 300 chars")

class Diagnostics(BaseModel):
    latency_ms: int
    model: str
    tokens_in: int
    tokens_out: int
    estimated_cost_usd: float

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    status: Literal["answered", "insufficient_evidence", "needs_clarification"]
    citations: List[Citation] = Field(default_factory=list)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    diagnostics: Diagnostics

class HealthResponse(BaseModel):
    ok: bool
    documents_indexed: int
    model: str
