# CORPUS_NOTES.md: Analysis of the Ferrowave Documentation

This document records the empirical observations, formatting peculiarities, contradictions, and structural risks discovered while parsing, indexing, and querying the 41 documents in `corpus/`.

---

## 1. Heterogeneous File Formats

The corpus mimics a realistic company wiki developed over several years across multiple departments:
- **Markdown (`.md`)**: 28 files. Well-structured, but inconsistent heading levels.
- **Plain Text (`.txt`)**: `support/help-center-troubleshooting.txt`. Unstructured, bullet points and internal agent tips.
- **HTML (`.html`)**: `product-docs/api-rate-limits.html` and `trust/trust-center-faq.html`. Contains `<table>` elements and nested markup requiring strip-and-table parsing.
- **CSV (`.csv`)**: `product-docs/integrations.csv`. Structured catalog of third-party connectors, authentication methods, and plan availability.
- **JSON (`.json`)**: `pricing/plans.json`. Machine-readable plan matrix with tier limits, add-on pricing, and quotas.
- **PDF (`.pdf`)**: `legal/terms-of-service.pdf`. Multi-page formal legal document; requires text extraction with page tracking.
- **Word Document (`.docx`)**: `legal/dpa.docx`. Standard Data Processing Addendum with formal tabular schedules.

---

## 2. Audience Boundaries & Confidentiality Risks

`_manifest.csv` designates three files as `audience: internal`:
1. `policies/sla-v4-DRAFT.md` (`status: draft`): Contains proposed SLA uptime numbers (99.95%) not yet approved. If exposed, customers could demand SLA credits based on unratified numbers.
2. `internal/rfc-0042-salesforce-v2.md` (`status: current`): Internal architectural proposal detailing internal API endpoints, database schemas, and migration risks.
3. `internal/support-macros.md` (`status: current`): Internal support canned responses, escalation procedures, and internal refund discretion thresholds.

**Architectural Decision**: The engine enforces a strict filter in `app/manifest.py` and `app/retriever.py`: any document with `audience == "internal"` or `status == "draft"` is quarantined from customer-facing retrieval.

---

## 3. Contradictions and Supersession

1. **Pricing Supersession (2024 vs 2026)**:
   - `pricing/pricing-2024.md` (superseded 1 March 2026) listed Starter at $39/mo, Growth at $89/mo.
   - `pricing/pricing-2026.md` (current) lists Starter at $49/mo, Growth at $99/mo.
   - `blog/2026-02-pricing-update.md` introduces grandfathering rules (existing accounts stay on 2024 pricing until 1 March 2027).
   - **Resolution**: The retriever heavily discounts superseded documents unless the query explicitly asks about historical pricing or grandfathering.

2. **Refund Policy Precedence Conflict**:
   - `support/faq.md` (dated 2023-11-02) stated: *"You can request a refund within 30 days of any billing event."*
   - `policies/refund-policy.md` (v3, approved 10 Feb 2026) Section 1.2 states: *"Monthly renewal charges are not refundable."*
   - Section 0 of the Refund Policy explicitly states: *"If anything in our help articles, FAQ pages, marketing pages, or community forum conflicts with this policy or the Terms of Service, this policy and the Terms of Service prevail."*
   - **Resolution**: Our engine assigns priority weight 100 to `policies/refund-policy.md` and 50 to FAQ articles, guaranteeing policy documents override conflicting help content.

---

## 4. Recommendations for Ferrowave Documentation Team

1. **Deprecate Outdated FAQ Pages**: `support/faq.md` has not been updated since November 2023 and directly contradicts Refund Policy v3.
2. **Unified Legal Source of Truth**: Terms of Service and DPA should be maintained in source-controlled markdown rather than binary formats (.pdf / .docx) to enable continuous automated drift detection.
3. **Formal Plan Taxonomy**: Some docs refer to "Starter / Growth / Scale / Enterprise" while older release notes mention "Free Tier" or "Professional Tier".
