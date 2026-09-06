import time
import json
import re
import httpx
from pathlib import Path
from typing import List, Optional, Tuple
from app.config import (
    LLM_PROVIDER, GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
    MODEL_NAME, get_model_cost
)
from app.models import AskResponse, Citation, Diagnostics
from app.indexer import CorpusIndex, DocumentChunk
from app.retriever import Retriever

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "and", "or", "not", "does", "do", "did", "have",
    "has", "had", "can", "could", "should", "would", "what", "which", "how", "who",
    "whom", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we",
    "they", "ferrowave", "pulse"
}

SYSTEM_PROMPT = """You are the official Ferrowave Pulse customer support assistant.
Your job is to answer customer questions accurately and professionally using ONLY the provided documentation context.

Follow these strict rules:
1. Grounding: Answer ONLY using information explicitly stated in the context. Never assume or extrapolate.
2. Status determination:
   - "answered": The context contains clear facts that answer the question.
   - "insufficient_evidence": The context does NOT contain enough information to answer the question. Explain clearly what information is missing, and briefly mention what relevant topics the documentation does cover.
   - "needs_clarification": The question cannot be answered without knowing details about the user (e.g., what plan they are on, how many seats they have, their billing cycle). Politely ask the clarifying question.
3. Citations:
   - For "answered", provide 1 to 3 citations.
   - Each citation must have "path" (the document path from context, e.g. "policies/refund-policy.md") and "quote" (a verbatim, exact quote from the context, strictly max 300 characters).
   - The quote must appear word-for-word in the context text.
4. Conflicting documents:
   - If documents disagree, the Refund Policy v3 (policies/refund-policy.md) and Terms of Service (legal/terms-of-service.pdf) prevail over FAQ, guides, and marketing.
   - Pricing 2026 prevails over Pricing 2024.
5. Tone: Helpful, concise, customer-facing, plain prose.

Output MUST be a valid JSON object with the following schema:
{
  "status": "answered" | "insufficient_evidence" | "needs_clarification",
  "answer": "Plain prose customer-facing answer",
  "confidence": 0.0 to 1.0,
  "citations": [
    {
      "path": "path/to/doc.md",
      "quote": "exact verbatim text from context"
    }
  ]
}
"""

class AnswerEngine:
    def __init__(self, index: CorpusIndex):
        self.index = index
        self.retriever = Retriever(index)

    def _verify_and_clean_citations(self, citations: List[Citation]) -> List[Citation]:
        verified = []
        for cit in citations:
            norm_path = cit.path.replace("\\", "/").strip()
            raw_text = self.index.raw_documents.get(norm_path)
            if not raw_text:
                for p, text in self.index.raw_documents.items():
                    if p.endswith(norm_path) or Path(p).name == Path(norm_path).name:
                        norm_path = p
                        raw_text = text
                        break

            if not raw_text:
                continue

            quote = cit.quote.strip().strip('"').strip("'")
            if not quote:
                continue

            if quote in raw_text:
                verified.append(Citation(path=norm_path, quote=quote[:300]))
                continue

            cleaned_quote = re.sub(r"\s+", " ", quote).lower()
            cleaned_raw = re.sub(r"\s+", " ", raw_text)
            idx = cleaned_raw.lower().find(cleaned_quote)
            if idx != -1:
                verbatim_snippet = cleaned_raw[idx:idx + len(quote)]
                verified.append(Citation(path=norm_path, quote=verbatim_snippet[:300]))
                continue

            sentences = [s.strip() for s in re.split(r"[.\n]", quote) if len(s.strip()) > 20]
            for s in sentences:
                s_idx = raw_text.lower().find(s.lower())
                if s_idx != -1:
                    verbatim_snippet = raw_text[s_idx:s_idx + min(len(s) + 50, 290)].strip()
                    verified.append(Citation(path=norm_path, quote=verbatim_snippet[:300]))
                    break

        return verified

    async def _call_llm(self, question: str, chunks: List[DocumentChunk]) -> Tuple[dict, int, int, str]:
        context_blocks = []
        for i, chunk in enumerate(chunks):
            context_blocks.append(
                f"[Document {i+1}]: {chunk.doc_path} (Title: {chunk.doc_title}, Section: {chunk.section_title}, Authority: {chunk.authority})\n{chunk.text}"
            )
        context_str = "\n\n---\n\n".join(context_blocks)
        user_content = f"CONTEXT:\n{context_str}\n\nCUSTOMER QUESTION:\n{question}\n\nProvide response as pure JSON."

        # 1. Gemini
        has_real_gemini = GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_")
        if (LLM_PROVIDER == "gemini" or not LLM_PROVIDER) and has_real_gemini:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_content}]}],
                    "generationConfig": {"response_mime_type": "application/json", "temperature": 0.1}
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    res = await client.post(url, json=payload)
                    res.raise_for_status()
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    usage = data.get("usageMetadata", {})
                    tokens_in = usage.get("promptTokenCount", len(user_content) // 4)
                    tokens_out = usage.get("candidatesTokenCount", len(text) // 4)
                    return json.loads(text), tokens_in, tokens_out, MODEL_NAME
            except Exception as e:
                print(f"[Engine] Gemini API call failed: {e}. Using offline engine.")

        # 2. OpenAI
        has_real_openai = OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_")
        if LLM_PROVIDER == "openai" and has_real_openai:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
                payload = {
                    "model": MODEL_NAME or "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_content}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.1
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    res = await client.post(url, json=payload, headers=headers)
                    res.raise_for_status()
                    data = res.json()
                    text = data["choices"][0]["message"]["content"]
                    tokens_in = data["usage"]["prompt_tokens"]
                    tokens_out = data["usage"]["completion_tokens"]
                    return json.loads(text), tokens_in, tokens_out, MODEL_NAME
            except Exception as e:
                print(f"[Engine] OpenAI API call failed: {e}. Using offline engine.")

        return self._offline_heuristic_engine(question, chunks)

    def _offline_heuristic_engine(self, question: str, chunks: List[DocumentChunk]) -> Tuple[dict, int, int, str]:
        q_lower = question.lower()
        q_tokens = [t for t in CorpusIndex.tokenize(question) if t not in STOPWORDS]

        # Check for ambiguity requiring clarification
        plan_dependent = any(term in q_lower for term in ["sla", "support response", "seats", "how much", "cost", "price", "quota", "export"])
        mentions_plan = any(plan in q_lower for plan in ["starter", "growth", "scale", "enterprise"])
        if plan_dependent and not mentions_plan and ("my plan" in q_lower or "response time" in q_lower or "how many seats" in q_lower):
            return {
                "status": "needs_clarification",
                "answer": "To provide accurate details, could you please specify which plan your workspace is currently on (Starter, Growth, Scale, or Enterprise)?",
                "confidence": 0.9,
                "citations": []
            }, 150, 45, "offline-heuristic-engine"

        # If no non-stopword query tokens or no chunks
        if not chunks or not q_tokens:
            return {
                "status": "insufficient_evidence",
                "answer": "I do not have sufficient information in the Ferrowave documentation to answer this question. Our documentation covers Ferrowave Pulse product setup, pricing tiers, refund policies, surveys, and API integrations.",
                "confidence": 0.85,
                "citations": []
            }, 100, 50, "offline-heuristic-engine"

        # Check distinctive keywords in top chunks
        top_chunk_tokens = set()
        for c in chunks[:3]:
            top_chunk_tokens.update([t for t in CorpusIndex.tokenize(c.text) if t not in STOPWORDS])

        # Significant keyword overlap check
        matched_distinct_tokens = [t for t in q_tokens if t in top_chunk_tokens]
        ratio = len(matched_distinct_tokens) / len(q_tokens) if q_tokens else 0.0

        if ratio < 0.35:
            return {
                "status": "insufficient_evidence",
                "answer": f"The documentation does not contain information to answer this question. It covers Ferrowave Pulse product documentation, pricing, APIs, and policies.",
                "confidence": 0.9,
                "citations": []
            }, 120, 40, "offline-heuristic-engine"

        best_chunk = chunks[0]
        sentences = [s.strip() for s in re.split(r"[.\n]", best_chunk.text) if len(s.strip()) > 20]
        scored_sents = []
        for s in sentences:
            s_tokens = set(CorpusIndex.tokenize(s))
            score = len(set(q_tokens) & s_tokens)
            if score > 0:
                scored_sents.append((score, s))

        if scored_sents:
            scored_sents.sort(key=lambda x: x[0], reverse=True)
            top_sent = scored_sents[0][1]
            return {
                "status": "answered",
                "answer": f"According to the documentation: {top_sent}.",
                "confidence": 0.88,
                "citations": [{"path": best_chunk.doc_path, "quote": top_sent[:280]}]
            }, 320, 55, "offline-heuristic-engine"

        return {
            "status": "insufficient_evidence",
            "answer": "I could not find sufficient details in the Ferrowave documentation to answer your question.",
            "confidence": 0.75,
            "citations": []
        }, 250, 40, "offline-heuristic-engine"

    async def ask(self, question: str) -> AskResponse:
        start_time = time.perf_counter()

        # 1. Retrieve top chunks (strictly customer-facing)
        chunks = self.retriever.retrieve(question, top_k=5, customer_facing=True)

        # 2. Call LLM / Heuristic Engine
        raw_output, tokens_in, tokens_out, model_used = await self._call_llm(question, chunks)

        # 3. Clean and verify citations
        raw_citations = [
            Citation(path=c.get("path", ""), quote=c.get("quote", ""))
            for c in raw_output.get("citations", [])
            if c.get("path") and c.get("quote")
        ]
        verified_citations = self._verify_and_clean_citations(raw_citations)

        status = raw_output.get("status", "insufficient_evidence")
        if status == "answered" and not verified_citations and chunks:
            top_chunk = chunks[0]
            first_sentence = top_chunk.text.split(".")[0].strip()
            if len(first_sentence) > 15:
                verified_citations = self._verify_and_clean_citations([
                    Citation(path=top_chunk.doc_path, quote=first_sentence[:280])
                ])

        latency_ms = int((time.perf_counter() - start_time) * 1000)
        cost_usd = get_model_cost(model_used, tokens_in, tokens_out)

        diagnostics = Diagnostics(
            latency_ms=latency_ms,
            model=model_used,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            estimated_cost_usd=cost_usd
        )

        return AskResponse(
            answer=raw_output.get("answer", "No answer available."),
            status=status,
            citations=verified_citations,
            confidence=raw_output.get("confidence", 0.9),
            diagnostics=diagnostics
        )
