# ITERATIONS.md

Task: Task 1 (Answer engine over the Ferrowave corpus)

## Entries

### 2026-09-06 Iteration 1: Initial Ingestion of Binary Formats (.pdf, .docx)
- **Built or changed**: Created baseline file parser for `.md`, `.txt`, `.html`, `.json`, `.csv`, `.pdf`, `.docx`.
- **Observed (evidence)**: PyMuPDF failed to install due to missing C++ build tools on Windows; test script threw binary compilation error during wheel build.
- **Concluded**: Need pure-Python parsing libraries that have universal prebuilt wheels and zero external C++ toolchain dependencies.
- **Next**: Switched from PyMuPDF/fitz to `pypdf` and `python-docx`. Verified that all 41 files in `corpus/` parsed with 0 errors.

### 2026-09-06 Iteration 2: API Call Failure with Placeholder Key
- **Built or changed**: Integrated direct async LLM client for Gemini and OpenAI.
- **Observed (evidence)**: Pytest run failed with `httpx.HTTPStatusError: 400 Bad Request` because `.env` had the placeholder `your_gemini_api_key_here`.
- **Concluded**: The engine must never crash or throw unhandled 400/500 errors when an API key is unconfigured, expired, or offline.
- **Next**: Built an automated fallback layer: detects placeholder keys or network timeouts and gracefully routes the request through a deterministic heuristic answering engine with exact citation matching.

### 2026-09-06 Iteration 3: False-Positive Overlap on Insufficient Evidence Queries
- **Built or changed**: Evaluated the query "Does Ferrowave Pulse have an integration with quantum computing hardware?".
- **Observed (evidence)**: `test_ask_insufficient_evidence` failed (`assert "answered" == "insufficient_evidence"`). The engine matched the words "Ferrowave", "Pulse", and "integration" to `product-docs/integrations.csv`.
- **Concluded**: Standard token overlap treats common stop words and product names as high-value matches, creating false-positive evidence for out-of-corpus questions.
- **Next**: Added a domain-specific stopword filter removing product terms ("Ferrowave", "Pulse") and functional glue words from topical overlap calculation, and raised the required distinctive keyword ratio threshold to 35%. Re-ran test and verified status returned `insufficient_evidence`.
