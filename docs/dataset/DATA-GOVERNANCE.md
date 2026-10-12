# Data Governance & Source-of-Truth Architecture

## 1. Governance Principles

The **Smart GST System** enforces strict data governance rules across all dataset stores:

> **Data Integrity Policy**: *Never invent or hallucinate HSN codes, SAC codes, or GST tax rates. Demo data MUST be clearly badged as "DEMO DATA / TEST FIXTURE" and prevented from masquerading as production data.*

---

## 2. Source-of-Truth Hierarchy

1. **Tier 1 (Authoritative)**: Central Board of Indirect Taxes and Customs (CBIC) Official Notifications & Schedules (`cbic-gst.gov.in`).
2. **Tier 2 (Official Gazette)**: Official Gazette of India (`egazette.gov.in`).
3. **Tier 3 (GST Council)**: Official GST Council meeting recommendations & rate decisions (`gstcouncil.gov.in`).
4. **Forbidden**: Commercial blogs or unverified third-party rate aggregators are strictly prohibited as primary sources.

---

## 3. Effective Date & Historical Versioning

When CBIC issues a notification updating a rate or schedule entry:
- The previous rule version's `effective_to` date is updated to the day prior to the new notification's launch.
- The new rule version is inserted with `effective_from` set to the new date and `effective_to = null`.
- Historical entries are never overwritten or deleted, ensuring retroactive audit capabilities.
