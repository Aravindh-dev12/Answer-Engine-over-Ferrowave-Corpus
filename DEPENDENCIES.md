# DEPENDENCIES.md

Task: Task 1 (Answer engine over the Ferrowave corpus)

Every third-party package added beyond Python standard library:

| Package | Version | What it does for me here | What I would have to write if it were removed | Risk (size, maintenance, licence, lock-in) |
|---|---|---|---|---|
| `fastapi` | 0.141.1 | High-performance ASGI framework handling HTTP endpoints and Pydantic validation. | A custom WSGI/ASGI router on `http.server` or `wsgiref` plus manual JSON schema validation. | Low risk; BSD license, industry standard. |
| `uvicorn` | 0.52.4 | Production ASGI server running the FastAPI application. | A custom asyncio TCP server handling HTTP/1.1 protocol framing. | Low risk; BSD license, actively maintained. |
| `pydantic` | 2.13.5 | Strict schema definition and type validation for requests and responses. | Hand-written dictionary validators with type-checking and bounds checks. | Low risk; MIT license. |
| `httpx` | 0.28.1 | Async HTTP client for communicating with LLM provider APIs. | Custom `urllib.request` wrapper or raw `http.client` implementation. | Low risk; BSD license. |
| `rank_bm25` | 0.2.2 | Pure-Python Okapi BM25 implementation for lexical document retrieval. | A 60-line BM25 ranking algorithm calculating term frequency, inverse document frequency, and document length normalization. | Low risk; MIT license, stable math. |
| `pypdf` | 6.17.0 | Pure Python PDF parser for extracting text from `legal/terms-of-service.pdf`. | Complex PDF stream decompresor and font operator parser. | Low risk; BSD-3 license. |
| `python-docx`| 1.2.0 | XML parser for extracting text and tables from `legal/dpa.docx`. | Direct `zipfile` extraction and XML DOM parser over `word/document.xml`. | Low risk; MIT license. |
| `beautifulsoup4` | 4.15.0 | HTML parser for extracting text and tables from HTML files. | A stateful `html.parser.HTMLParser` subclass with stack-based tag tracking. | Low risk; MIT license. |
| `python-dotenv` | 1.2.3 | Loads environment variables from `.env` file into `os.environ`. | A 10-line text reader splitting lines on `=` into `os.environ`. | Negligible risk; BSD license. |
| `pytest` | 9.1.1 | Test execution framework. | `unittest` from Python standard library. | Development dependency only. |
