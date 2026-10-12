# Software Requirements Specification (SRS)

## 1. Problem Statement & Scope

The **Smart GST Verifier & Compliance Engine** addresses indirect tax classification and rate calculation challenges in Indian commerce. Businesses must accurately map commercial trade descriptions to 8-digit Harmonized System of Nomenclature (HSN) codes (for Goods) or 6-digit Services Accounting Codes (SAC) (for Services), calculate CGST/SGST/IGST rates, and issue compliant tax invoices under Rule 46 of the CGST Rules, 2017.

---

## 2. Actors & System Roles

| Actor ID | Role Name | System Privileges & Responsibilities |
| :--- | :--- | :--- |
| **ACT-01** | `USER` (Taxpayer / Sales Executive) | Submits product trade descriptions, views HSN/SAC classification, inspects evidence-backed explanations, and generates tax invoices. |
| **ACT-02** | `COMPLIANCE_OFFICER` | Reviews flagged ambiguous items, inspects audit logs, and validates statutory source citations. |
| **ACT-03** | `ADMIN` (System Administrator) | Manages canonical HSN/SAC codes, statutory GST rate rules, CBIC source documents, vector indexing, and Neo4j graph synchronization. |

---

## 3. System Functional Requirements Summary

The system fulfills 10 core functional domains (FR-001 through FR-015) spanning product preprocessing, hybrid candidate retrieval, Neo4j graph reasoning, grounded RAG synthesis, explainable decision AI, deterministic tax reconciliation, sales invoicing, audit trails, and administrative governance. Detailed requirements are cataloged in [`docs/requirements/FUNCTIONAL_REQUIREMENTS.md`](docs/requirements/FUNCTIONAL_REQUIREMENTS.md).

---

## 4. Non-Functional Requirements Summary

Enforces performance thresholds (NFR-001 through NFR-010) including <2s API latency, HMAC-SHA256 token security, sliding-window rate limiting, multi-viewport responsiveness (320px-1920px), and zero LLM fact hallucination. Detailed specifications are cataloged in [`docs/requirements/NON_FUNCTIONAL_REQUIREMENTS.md`](docs/requirements/NON_FUNCTIONAL_REQUIREMENTS.md).
