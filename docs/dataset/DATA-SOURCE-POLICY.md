# Authoritative Data Source & Provenance Policy

## 1. Provenance Requirements

Every record in the authoritative dataset MUST store provenance fields:
- `source_name`: Authority publisher (e.g. `CBIC`)
- `source_url`: Direct HTTPS link to official PDF/Gazette document
- `notification_number`: Official notification identifier (e.g. `1/2017-Central Tax (Rate)`)
- `notification_date`: Official publication date

---

## 2. Ingestion & Validation Policy

1. **Deterministic Ingestion**: Ingested entries are checked for duplicate HSN/SAC codes, mathematical rate consistency ($\text{CGST} + \text{SGST} = \text{GST}$), and date range validity.
2. **Graceful Fail-Closed Behavior**: If source provenance cannot be established or verified, the system sets `verification_status = REQUIRES_REVIEW` rather than displaying ungrounded data.
