# System User Stories Specification

## User Story Catalog

| Story ID | Persona / Role | User Story (As a... I want to... So that...) | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **US-001** | Taxpayer | As a Taxpayer, I want to input natural-language trade terms so that I can find the canonical 8-digit HSN code without memorizing tariff schedules. | System returns 8-digit HSN code, GST rate, and confidence score. |
| **US-002** | Business Owner | As a Business Owner, I want to automatically generate GST tax invoices with correct CGST/SGST vs IGST breakdown so that I stay compliant under Rule 46. | Invoice module calculates taxable values and tax splits deterministically. |
| **US-003** | Auditor | As a Tax Auditor, I want every classification result to display verified CBIC source citations so that I can verify legal evidence provenance. | Evidence section displays notification number, effective dates, and citation links. |
| **US-004** | Compliance Officer | As a Compliance Officer, I want low confidence or ambiguous items flagged for human review so that incorrect tax payments are prevented. | Items with score gap < 0.15 flag `REQUIRES_HUMAN_REVIEW`. |
| **US-005** | Administrator | As an Admin, I want to manage statutory GST rules via an administrative panel that requires RBAC and logs audit events so that unauthorized rule changes are blocked. | `/api/v1/admin/*` endpoints return 403 Forbidden for non-admins and write an `AuditLog`. |
