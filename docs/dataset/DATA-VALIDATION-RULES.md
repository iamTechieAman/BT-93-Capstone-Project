# Dataset Validation Rules & Automated Check Engine

## 1. Validation Rule Set

The automated dataset validator ([`scripts/validate_dataset.py`](scripts/validate_dataset.py)) enforces 8 mandatory integrity checks:

| Rule Code | Validation Check Description | Action on Failure |
| :--- | :--- | :--- |
| **RULE-01** | **Schema Completeness**: All 27 required schema fields must be present. | Reject record |
| **RULE-02** | **Code Format & Level**: `code` must be 2, 4, 6, or 8 digits matching `code_type`. | Reject record |
| **RULE-03** | **Hierarchy Consistency**: Chapter (2-digit) and Heading (4-digit) must match code prefix. | Reject record |
| **RULE-04** | **Duplicate Detection**: Flag duplicate HSN/SAC code entries. | Emit Warning / Deduplicate |
| **RULE-05** | **Tax Math Consistency**: $\text{CGST} + \text{SGST} == \text{GST}$ and $\text{IGST} == \text{GST}$. | Reject record |
| **RULE-06** | **Source Provenance**: `source_document` and valid HTTPS `source_url` are mandatory. | Reject record |
| **RULE-07** | **Effective Date Validity**: `effective_from` $\le$ `effective_to`. | Reject record |
| **RULE-08** | **Status Classification**: `verification_status` must be valid enum. | Reject record |

---

## 2. Repeatable Validation Script Execution

Run the automated dataset validation engine:

```bash
python3 scripts/validate_dataset.py
```
