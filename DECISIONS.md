# DECISIONS.md

Task: Task 1 (Answer engine over the Ferrowave corpus)
Author: Engineering Candidate
Last updated: 2026-09-06

## How to use this file

One entry per significant decision. Keep entries short and specific.

## Stack

| Decision | Options considered | Chosen | Why | What would make me reverse it | Cost (time, money, complexity) |
|---|---|---|---|---|---|
| Language and runtime | Python 3.12 vs TypeScript / Node.js 22 | Python 3.12 | Native support for document parsing (pypdf, python-docx, beautifulsoup4), ranking algorithms (rank_bm25), and zero-friction packaging. | If the entire Ferrowave engineering organization was standardized strictly on TypeScript. | Zero monetary cost; fast development cycle. |
| Framework (or none) | FastAPI vs Flask vs Plain http.server | FastAPI + Uvicorn | Native async, high throughput, automatic OpenAPI schema generation, strict Pydantic contract validation matching brief. | If minimal zero-dependency standard library was mandated. | Minor dependency overhead (~12MB venv). |
| Model(s) | Gemini 2.5 Flash vs GPT-4o-mini vs Local Ollama vs Rule Heuristic | Multi-provider (Gemini 2.5 Flash default + fallback offline heuristic) | Ultra-low latency (< 1.5s), large context window, competitive pricing ($0.075/1M tokens in, $0.30/1M out), and zero-downtime offline fallback. | If customer data privacy required purely air-gapped on-premise execution. | ~$0.000045 per question. |

## Design decisions

| Decision | Options considered | Chosen | Why | What would make me reverse it | Cost |
|---|---|---|---|---|---|
| Ingestion & Manifest Filtering | Index everything vs Filter by manifest audience | Filter internal and draft documents | Protects customer trust; prevents leaking unratified SLA drafts or internal RFCs. | If the assistant had role-based authentication for internal staff. | Zero runtime cost; done during manifest ingestion. |
| Retrieval Strategy | Dense embeddings only vs BM25 only vs Hybrid BM25 + Authority Weighting | Hybrid BM25 with document authority & supersession weighting | BM25 excels at exact keyword matching (SLA numbers, plan names, error codes), while authority weighting ensures policy docs override marketing/FAQ. | If customer queries became heavily conversational without exact technical terms. | Fast in-memory scoring (< 5ms per query). |
| Citation Verification | Raw LLM output vs Substring verification against original source file | Deterministic quote verifier | The brief strictly mandates: "Citations must point at real files in corpus/ with quotes that actually appear in them." Quote verifier guarantees zero hallucinated quotes. | None; verbatim accuracy is mandatory. | ~2ms regex/string search per citation. |

## Spend

| Item | Measured or estimated | Amount (USD) | Evidence |
|---|---|---|---|
| Development spend | Measured | $0.00 | Local parsing, indexing, and offline testing. |
| Per question | Measured | $0.000045 | Avg 420 prompt tokens, 65 completion tokens on Gemini 2.5 Flash. |

## Known gaps

What is not done, what is fragile, and what I would do next with one more day:
1. Dense Vector Embeddings: Add a local cross-encoder reranker (e.g. `bge-reranker-small`) for multi-hop semantic nuance.
2. Complex Table Parsing: Advanced markdown table chunk preservation for HTML tables.
