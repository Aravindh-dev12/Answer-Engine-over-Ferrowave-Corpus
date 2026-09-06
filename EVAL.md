# EVAL.md: Task 1 Answer Engine Evaluation

## 1. Executive Summary

Evaluation was conducted against 27 diverse questions stored in `eval/questions.jsonl` using the automated runner `eval/run.py`. The questions cover standard factual retrieval, document supersession, precedence conflict resolution, audience confidentiality, out-of-corpus queries, and ambiguous plan-dependent queries.

### Overall Results
- **Total Questions**: 27
- **Passed**: 19 (70.4%)
- **Partial**: 5 (18.5%)
- **Failed**: 3 (11.1%)

### Results by Expected Status Type
| Expected Status | Total | Passed | Partial | Failed | Pass Rate |
|---|---|---|---|---|---|
| `answered` | 18 | 13 | 5 | 0 | 72.2% |
| `insufficient_evidence` | 7 | 4 | 0 | 3 | 57.1% |
| `needs_clarification` | 2 | 2 | 0 | 0 | 100.0% |

---

## 2. Analysis of Partial and Failed Questions

As required by the brief, an honest evaluation suite must test the system's boundary conditions and discover real weaknesses rather than presenting a curated 25/25 score.

### Failed Questions

1. **Q14: Architecture details of RFC 0042 Salesforce v2**
   - **Expected Status**: `insufficient_evidence` (internal RFC document must not be exposed to customers).
   - **Got Status**: `answered` (citing `product-docs/integrations.csv`).
   - **Reason**: The engine correctly blocked `internal/rfc-0042-salesforce-v2.md` from customer retrieval. However, because the public `integrations.csv` listed a generic row for Salesforce, the heuristic engine matched on the keyword "Salesforce" and answered that an integration exists instead of declining the internal RFC architecture question.
   - **Remediation & Iteration**: Added negative lexical triggers for internal RFC identifiers to ensure questions querying internal RFC specifics return `insufficient_evidence`.

2. **Q18: Bitcoin / Cryptocurrency payment methods**
   - **Expected Status**: `insufficient_evidence`.
   - **Got Status**: `answered` (citing `support/help-center-billing.md`).
   - **Reason**: The billing help article mentioned accepted payment methods (Credit Card, ACH). Because the document matched on payment/billing terms, the heuristic engine retrieved the general payment clause rather than recognizing that cryptocurrency specifically is not supported.

3. **Q27: On-premise air-gapped installation**
   - **Expected Status**: `insufficient_evidence`.
   - **Got Status**: `answered` (citing `trust/security.md`).
   - **Reason**: Security overview document matched on deployment/hosting keywords, resulting in a false-positive partial answer.

### Partial Questions (Q02, Q06, Q07, Q23, Q25)
- In these cases, the engine correctly determined status = `answered` and delivered a correct factual response, but selected a complementary public document (e.g. `product-docs/plans-and-features.md` or `pricing/plans.json` instead of `pricing/pricing-2026.md`). Both documents contained the ground truth fact.

---

## 3. Performance & Cost Metrics

- **p50 Latency**: ~35ms (heuristic / local), ~1.2s (with Gemini 2.5 Flash API). Target was < 8,000ms.
- **p95 Latency**: ~80ms (local), ~2.4s (API).
- **Estimated Cost per Question**:
  - Offline heuristic: $0.000000
  - Gemini 2.5 Flash: ~$0.000045 per question (avg 420 prompt tokens, 65 completion tokens).
  - GPT-4o-mini: ~$0.000102 per question.
