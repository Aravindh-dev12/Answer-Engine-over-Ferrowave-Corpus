# AI_USAGE.md

Task: Task 1 (Answer engine over the Ferrowave corpus)

## Tools and models used

| Tool or model | Used for |
|---|---|
| Claude 3.5 Sonnet / Gemini 3.8 Flash | Drafting initial boilerplate schemas, regex patterns, and question variations. |

## At least three things an AI produced that were wrong or that I changed

1. **Hallucinated Citations in Prompt Output**:
   - *What it produced*: The AI prompt output generated quotes that summarized or paraphrased the source text (e.g. "Monthly renewals cannot be refunded") instead of reproducing the exact verbatim sentence from the document.
   - *Why it was wrong*: The Candidate Brief requirement 1 strictly dictates: "Citations must point at real files in corpus/ with quotes that actually appear in them." Paraphrases fail this test.
   - *What I did instead*: Built `_verify_and_clean_citations()` in `app/engine.py`. This layer takes every proposed citation, verifies it against the original raw document text, replaces it with the exact verbatim substring, and discards any citation that cannot be verified.

2. **Naïve Ingestion of Internal Documents**:
   - *What it produced*: An initial suggested indexing script walked all files in `corpus/` recursively and added everything to the searchable vector index.
   - *Why it was wrong*: Documents like `policies/sla-v4-DRAFT.md`, `internal/rfc-0042-salesforce-v2.md`, and `internal/support-macros.md` are marked `internal` or `draft` in `_manifest.csv`. Exposing them allows internal architecture and unapproved SLA commitments to leak to customers.
   - *What I did instead*: Introduced `ManifestRegistry` with `is_customer_accessible()`, which explicitly checks audience and status and quarantines internal/draft files from customer retrieval.

3. **Missing Precedence Hierarchy in Document Disagreements**:
   - *What it produced*: The AI suggested ranking retrieved documents purely by semantic vector distance, ignoring document status and authority.
   - *Why it was wrong*: Outdated FAQ articles (from 2023) or 2024 pricing docs could out-rank the official Refund Policy v3 (2026) if the user query happened to share more words with the FAQ.
   - *What I did instead*: Hard-coded document authority scoring based on the legal clause in Section 0 of `policies/refund-policy.md` ("Refund Policy v3 prevails over help and FAQ content") and implemented explicit discounting of superseded documents.

## Parts I wrote or designed without AI assistance
- Precedence hierarchy and manifest authority weighting logic.
- Verbatim quote verifier and substring reconciliation against the raw document corpus.
- The evaluation dataset covering edge cases, internal leakage traps, and ambiguous multi-plan queries.
