# DATA_SOURCE_POLICY.md — Data Source & Provenance Policy

**Project**: Smart GST Verification and Manufacturing Sales Automation System  
**Document Identifier**: DSP-GST-2026-V2.4  
**Date**: October 8, 2026  

---

## 1. Authoritative Source Guidelines

1. **Government Primary Sources**:
   - All production HSN codes, chapter descriptions, and tax rates must originate directly from the **Central Board of Indirect Taxes and Customs (CBIC)** (`cbic-gst.gov.in`) and official GST Council notifications.
2. **Zero Fabrication**:
   - Synthetic or AI-generated HSN codes or GST rates are strictly forbidden in production datasets.
3. **Source Type Taxonomy**:
   - `AUTHORITATIVE_CBIC`: Official government tariff schedules and notifications.
   - `DEMO_SAMPLE`: Explicitly labeled test queries used strictly for UI testing and evaluation.

---

## 2. Provenance & Audit Metadata

Every record imported into `data/processed/` must preserve:
- Official document title (`source_document`).
- Direct government URL (`source_url`).
- Official notification number (`notification_number`).
- Effective date bounds (`effective_from` and `effective_to`).
- Retrieval timestamp (`retrieved_at`).
