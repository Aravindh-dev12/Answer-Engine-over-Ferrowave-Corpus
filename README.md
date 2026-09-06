# Ferrowave Pulse Answer Engine (Task 1)

A customer-facing, retrieval-augmented answer service that answers questions using only the Ferrowave documentation corpus, cites what it used with verbatim quotes, resolves document conflicts according to legal precedence, and knows when it should not answer.

---

## 1. Quick Start

### One-command run:
**Windows**:
```cmd
run.bat
```
**Linux / macOS**:
```bash
./run.sh
```

Or manually:
```bash
python -m venv .venv
# Activate virtual environment
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The service will be live at `http://127.0.0.1:8000`.

---

## 2. One-Command Re-indexing

To rebuild the index from the corpus directory (e.g. if a modified corpus is supplied during the live session):

**Windows**:
```cmd
reindex.bat
```
**Linux / macOS**:
```bash
./reindex.sh
```
Or directly:
```bash
python reindex.py --corpus corpus
```

---

## 3. API Contract

### Health Check
```bash
curl http://127.0.0.1:8000/health
```
Response:
```json
{
  "ok": true,
  "documents_indexed": 40,
  "model": "gemini-2.5-flash"
}
```

### Asking Questions
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"How many seats are included on the Scale plan?\"}"
```
Response:
```json
{
  "answer": "The Scale plan includes 25 seats.",
  "status": "answered",
  "citations": [
    {
      "path": "pricing/pricing-2026.md",
      "quote": "Scale includes 25 seats by default."
    }
  ],
  "confidence": 0.95,
  "diagnostics": {
    "latency_ms": 42,
    "model": "gemini-2.5-flash",
    "tokens_in": 380,
    "tokens_out": 45,
    "estimated_cost_usd": 0.000042
  }
}
```

---

## 4. Architecture & Key Features

1. **Multi-Format Ingestion**: Parses Markdown, Plain Text, HTML tables, CSV directories, JSON plan matrices, PDF legal documents, and Word `.docx` files.
2. **Confidentiality Filtering**: Reads `_manifest.csv` and strictly quarantines internal RFCs (`internal/rfc-0042-salesforce-v2.md`) and draft agreements (`policies/sla-v4-DRAFT.md`) from customer retrieval.
3. **Precedence Resolution**: Automatically favors current documents (`pricing-2026.md`) over superseded ones (`pricing-2024.md`), and enforces Refund Policy v3 over outdated FAQ articles.
4. **Verbatim Quote Verifier**: Enforces that all citations match exact substrings in the raw source files ($\le 300$ chars).
5. **Three Triage States**:
   - `answered`: Corpus provides sufficient factual backing.
   - `insufficient_evidence`: Question is outside corpus scope or queries internal data.
   - `needs_clarification`: Question requires user plan or account context.

---

## 5. Running Tests & Evaluation

### Automated Tests
```bash
pytest tests/
```

### Evaluation Suite (27 questions)
```bash
python eval/run.py
```
Detailed results and error analysis are generated in `eval/results.md` and summarized in `EVAL.md`.
