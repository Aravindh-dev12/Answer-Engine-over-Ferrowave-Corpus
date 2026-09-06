# Evaluation Results (Task 1)

- Total Questions: 27
- Passed: 19 (70.4%)
- Partial: 5 (18.5%)
- Failed: 3 (11.1%)

## Detailed Question Breakdown

| ID | Question | Expected Status | Got Status | Citations Count | Judgement | Reason |
|---|---|---|---|---|---|---|
| Q01 | Which channels can I use to deliver a survey in Ferrowave Pulse? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q02 | How many seats are included on the Scale plan? | answered | answered | 1 | **partial** | Correct status, but cited ['product-docs/plans-and-features.md'] instead of expected ['pricing/pricing-2026.md', 'pricing/plans.json']. |
| Q03 | How long are export files available for download after generation? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q04 | What is the target support response time on the Growth plan? | answered | answered | 1 | **partial** | Correct status, but cited ['product-docs/response-quotas.md'] instead of expected ['product-docs/plans-and-features.md']. |
| Q05 | Which events can webhooks send? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q06 | Can I get a refund on my monthly subscription renewal? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q07 | What is the monthly price of the Starter plan? | answered | answered | 1 | **partial** | Correct status, but cited ['blog/2026-02-pricing-update.md'] instead of expected ['pricing/pricing-2026.md']. |
| Q08 | What was the price of the Starter plan in 2024? | answered | answered | 1 | **partial** | Correct status, but cited ['blog/2026-02-pricing-update.md'] instead of expected ['pricing/pricing-2024.md']. |
| Q09 | What is the refund window for new monthly subscriptions? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q10 | What is the refund policy for annual subscriptions? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q11 | What is the target support response time for my account? | needs_clarification | needs_clarification | 0 | **pass** | Correctly classified as needs_clarification. |
| Q12 | How much will it cost to add extra seats to my plan? | needs_clarification | needs_clarification | 0 | **pass** | Correctly classified as needs_clarification. |
| Q13 | How long is customer survey response data retained in Ferrowave? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q14 | What are the architecture details of RFC 0042 Salesforce v2? | insufficient_evidence | insufficient_evidence | 0 | **pass** | Correctly classified as insufficient_evidence. |
| Q15 | What are the uptime commitments in the SLA v4 draft? | insufficient_evidence | answered | 1 | **fail** | Status mismatch: expected insufficient_evidence, got answered. |
| Q16 | What internal macros do Ferrowave support agents use? | insufficient_evidence | answered | 1 | **fail** | Status mismatch: expected insufficient_evidence, got answered. |
| Q17 | Does Ferrowave Pulse support HIPAA compliance and BAA agreements? | insufficient_evidence | answered | 1 | **fail** | Status mismatch: expected insufficient_evidence, got answered. |
| Q18 | Can I pay for Ferrowave Pulse using Bitcoin or cryptocurrency? | insufficient_evidence | insufficient_evidence | 0 | **pass** | Correctly classified as insufficient_evidence. |
| Q19 | How do I configure SAML SSO with Okta? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q20 | What happens if I exceed my monthly survey response quota? | answered | answered | 1 | **partial** | Correct status, but cited ['support/faq.md'] instead of expected ['product-docs/response-quotas.md']. |
| Q21 | What is the API rate limit for Growth tier customers? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q22 | How do webhook signatures work and what header is used? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q23 | What are the grandfathering rules for existing customers from the 2026 pricing update? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q24 | What are the rules for acceptable survey content under the Acceptable Use Policy? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q25 | Can I get an Enterprise trial without speaking to sales? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q26 | What is the SLA uptime guarantee for Enterprise customers? | answered | answered | 1 | **pass** | Correct status, valid factual answer and citations. |
| Q27 | Does Ferrowave provide an on-premise air-gapped installation? | insufficient_evidence | insufficient_evidence | 0 | **pass** | Correctly classified as insufficient_evidence. |

## Full Question Output Details

### Q01: Which channels can I use to deliver a survey in Ferrowave Pulse?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: Pulse can deliver a survey through:.
- **Citations**:
  - `product-docs/getting-started.md`: "Pulse can deliver a survey through:"

### Q02: How many seats are included on the Scale plan?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `partial` (Correct status, but cited ['product-docs/plans-and-features.md'] instead of expected ['pricing/pricing-2026.md', 'pricing/plans.json'].)
- **Answer**: According to the documentation: Pulse Alerts, which notify you when your score drops, are included on Growth, Scale, and.
- **Citations**:
  - `product-docs/plans-and-features.md`: "Pulse Alerts, which notify you when your score drops, are included on Growth, Scale, and"

### Q03: How long are export files available for download after generation?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: Every plan can export responses as CSV from the dashboard.
- **Citations**:
  - `product-docs/data-export.md`: "Every plan can export responses as CSV from the dashboard"

### Q04: What is the target support response time on the Growth plan?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `partial` (Correct status, but cited ['product-docs/response-quotas.md'] instead of expected ['product-docs/plans-and-features.md'].)
- **Answer**: According to the documentation: # Response quotas and overage.
- **Citations**:
  - `product-docs/response-quotas.md`: "# Response quotas and overage"

### Q05: Which events can webhooks send?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: Webhooks push events from Pulse to your systems as they happen.
- **Citations**:
  - `product-docs/webhooks.md`: "Webhooks push events from Pulse to your systems as they happen"

### Q06: Can I get a refund on my monthly subscription renewal?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: If you start a new monthly subscription and are not satisfied, you.
- **Citations**:
  - `policies/refund-policy.md`: "If you start a new monthly subscription and are not satisfied, you"

### Q07: What is the monthly price of the Starter plan?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `partial` (Correct status, but cited ['blog/2026-02-pricing-update.md'] instead of expected ['pricing/pricing-2026.md'].)
- **Answer**: According to the documentation: If you are on a **monthly** plan, your current price stays in place until your first.
- **Citations**:
  - `blog/2026-02-pricing-update.md`: "If you are on a **monthly** plan, your current price stays in place until your first"

### Q08: What was the price of the Starter plan in 2024?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `partial` (Correct status, but cited ['blog/2026-02-pricing-update.md'] instead of expected ['pricing/pricing-2024.md'].)
- **Answer**: According to the documentation: If you are on a **monthly** plan, your current price stays in place until your first.
- **Citations**:
  - `blog/2026-02-pricing-update.md`: "If you are on a **monthly** plan, your current price stays in place until your first"

### Q09: What is the refund window for new monthly subscriptions?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: If you start a new monthly subscription and are not satisfied, you.
- **Citations**:
  - `policies/refund-policy.md`: "If you start a new monthly subscription and are not satisfied, you"

### Q10: What is the refund policy for annual subscriptions?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: The refund is prorated: we refund the unused portion of the annual fee,.
- **Citations**:
  - `policies/refund-policy.md`: "The refund is prorated: we refund the unused portion of the annual fee,"

### Q11: What is the target support response time for my account?
- **Expected Status**: `needs_clarification` | **Got Status**: `needs_clarification`
- **Judgement**: `pass` (Correctly classified as needs_clarification.)
- **Answer**: To provide accurate details, could you please specify which plan your workspace is currently on (Starter, Growth, Scale, or Enterprise)?

### Q12: How much will it cost to add extra seats to my plan?
- **Expected Status**: `needs_clarification` | **Got Status**: `needs_clarification`
- **Judgement**: `pass` (Correctly classified as needs_clarification.)
- **Answer**: To provide accurate details, could you please specify which plan your workspace is currently on (Starter, Growth, Scale, or Enterprise)?

### Q13: How long is customer survey response data retained in Ferrowave?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: This article explains how long Ferrowave Pulse keeps the data you collect while your.
- **Citations**:
  - `policies/data-retention.md`: "This article explains how long Ferrowave Pulse keeps the data you collect while your"

### Q14: What are the architecture details of RFC 0042 Salesforce v2?
- **Expected Status**: `insufficient_evidence` | **Got Status**: `insufficient_evidence`
- **Judgement**: `pass` (Correctly classified as insufficient_evidence.)
- **Answer**: The documentation does not contain information to answer this question. It covers Ferrowave Pulse product documentation, pricing, APIs, and policies.

### Q15: What are the uptime commitments in the SLA v4 draft?
- **Expected Status**: `insufficient_evidence` | **Got Status**: `answered`
- **Judgement**: `fail` (Status mismatch: expected insufficient_evidence, got answered.)
- **Answer**: According to the documentation: This Service Level Agreement ("SLA") applies to Enterprise customers with a signed order.
- **Citations**:
  - `policies/sla-v3-approved.md`: "This Service Level Agreement ("SLA") applies to Enterprise customers with a signed order"

### Q16: What internal macros do Ferrowave support agents use?
- **Expected Status**: `insufficient_evidence` | **Got Status**: `answered`
- **Judgement**: `fail` (Status mismatch: expected insufficient_evidence, got answered.)
- **Answer**: According to the documentation: ## Do you support NPS, CSAT, and CES?.
- **Citations**:
  - `support/faq.md`: "## Do you support NPS, CSAT, and CES?"

### Q17: Does Ferrowave Pulse support HIPAA compliance and BAA agreements?
- **Expected Status**: `insufficient_evidence` | **Got Status**: `answered`
- **Judgement**: `fail` (Status mismatch: expected insufficient_evidence, got answered.)
- **Answer**: According to the documentation: Does Ferrowave sign HIPAA Business Associate Agreements?.
- **Citations**:
  - `trust/trust-center-faq.html`: "Does Ferrowave sign HIPAA Business Associate Agreements?"

### Q18: Can I pay for Ferrowave Pulse using Bitcoin or cryptocurrency?
- **Expected Status**: `insufficient_evidence` | **Got Status**: `insufficient_evidence`
- **Judgement**: `pass` (Correctly classified as insufficient_evidence.)
- **Answer**: I could not find sufficient details in the Ferrowave documentation to answer your question.

### Q19: How do I configure SAML SSO with Okta?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: SAML SSO is available on Scale and Enterprise plans.
- **Citations**:
  - `product-docs/sso-saml-setup.md`: "SAML SSO is available on Scale and Enterprise plans"

### Q20: What happens if I exceed my monthly survey response quota?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `partial` (Correct status, but cited ['support/faq.md'] instead of expected ['product-docs/response-quotas.md'].)
- **Answer**: According to the documentation: ## Can I use my own sending domain for email surveys?.
- **Citations**:
  - `support/faq.md`: "## Can I use my own sending domain for email surveys?"

### Q21: What is the API rate limit for Growth tier customers?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: API rate limits | Ferrowave Pulse Developer Docs.
- **Citations**:
  - `product-docs/api-rate-limits.html`: "API rate limits | Ferrowave Pulse Developer Docs"

### Q22: How do webhook signatures work and what header is used?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: Version 1 used the `X-Pulse-Signature` header with an HMAC-SHA1 of the body and no.
- **Citations**:
  - `product-docs/webhooks.md`: "Version 1 used the `X-Pulse-Signature` header with an HMAC-SHA1 of the body and no"

### Q23: What are the grandfathering rules for existing customers from the 2026 pricing update?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: # An update to Ferrowave Pulse pricing.
- **Citations**:
  - `blog/2026-02-pricing-update.md`: "# An update to Ferrowave Pulse pricing"

### Q24: What are the rules for acceptable survey content under the Acceptable Use Policy?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: # Acceptable Use Policy.
- **Citations**:
  - `policies/acceptable-use.md`: "# Acceptable Use Policy"

### Q25: Can I get an Enterprise trial without speaking to sales?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: # Community forum: Is there an Enterprise trial?.
- **Citations**:
  - `community/forum-enterprise-trial.md`: "# Community forum: Is there an Enterprise trial?"

### Q26: What is the SLA uptime guarantee for Enterprise customers?
- **Expected Status**: `answered` | **Got Status**: `answered`
- **Judgement**: `pass` (Correct status, valid factual answer and citations.)
- **Answer**: According to the documentation: This Service Level Agreement ("SLA") applies to Enterprise customers with a signed order.
- **Citations**:
  - `policies/sla-v3-approved.md`: "This Service Level Agreement ("SLA") applies to Enterprise customers with a signed order"

### Q27: Does Ferrowave provide an on-premise air-gapped installation?
- **Expected Status**: `insufficient_evidence` | **Got Status**: `insufficient_evidence`
- **Judgement**: `pass` (Correctly classified as insufficient_evidence.)
- **Answer**: The documentation does not contain information to answer this question. It covers Ferrowave Pulse product documentation, pricing, APIs, and policies.
