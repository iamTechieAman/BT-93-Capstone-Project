# Smart GST Statutory Evidence Validation Specification

## 1. Executive Summary

This document specifies the validation criteria, data structures, and empirical test requirements for the **Statutory Evidence Package Engine** in Phase 12.

Under project compliance rules, **no tax classification or rate determination is presented to the user without supporting statutory evidence**.

---

## 2. Mandatory Evidence Schema Fields

Every evidence item delivered by the verification pipeline must instantiate the 8 mandatory fields defined in [`EvidenceItem`](backend/app/schemas/gst_schema.py#L21-L34):

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `source` | `str` | Statutory issuing authority | `"Central Board of Indirect Taxes and Customs (CBIC)"` |
| `document` | `str` | Title of source document | `"GST Rate Schedule - Schedule III"` |
| `notification` | `str` | Gazette notification or circular number | `"Notification No. 1/2017-Central Tax (Rate)"` |
| `date` | `str` | Document issue / notification date | `"2017-06-28"` |
| `effective_period` | `str` | Legal effective period range | `"2017-07-01 to Present"` |
| `excerpt` | `str` | Direct excerpt / quotation from document | `"Heading 4203 applies to articles of apparel of leather. Rate is 18%."` |
| `url` | `str` | Clickable PDF / HTTP source link | `"https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf"` |
| `retrieved_at` | `str` | ISO 8601 retrieval timestamp | `"2026-10-09T02:15:00Z"` |

---

## 3. Evidence Audit Verification Workflow

```
[Verification Query]
       ↓
[HSN Retrieval Engine] ── [Extract HSN Master Record & Schedule]
       ↓
[Grounded RAG Search] ── [Retrieve Supporting CBIC Notification & Circular Chunks]
       ↓
[KG Ontology Traversal] ── [Validate Semantic Triples with Evidence Citations]
       ↓
[Evidence Audit Builder] ── [Enforce 8 Mandatory Schema Attributes per Item]
       ↓
[UI Audit Component] ── [Render Clickable Source Links & Detailed Parameter Grid]
```

---

## 4. Empirical Test Coverage & Assertions

Evidence integrity is automatically enforced by the backend test suite ([`backend/tests/test_confidence_and_evidence.py`](backend/tests/test_confidence_and_evidence.py)):

1. **Schema Completeness Test**: Asserts that `source`, `document`, `notification`, `effective_period`, `excerpt`, `url`, and `retrieved_at` are non-null for all evidence items.
2. **Provenance Citation Test**: Asserts that every evidence item contains valid statutory source URLs (`https://cbic-gst.gov.in/...`).
3. **Minimum Evidence Count Test**: Asserts that at least 4 independent evidence items are provided for every verification response.
