# Dataset Engineering Report

## Executive Summary

Phase 3 establishes a standardized, audit-ready GST & HSN Knowledge Dataset for the Smart GST Verification & Manufacturing Sales Automation System. To eliminate hallucinations and illegal tax calculations, the dataset architecture strictly separates **Authoritative CBIC Production Data** from **Demo/Sample Test Data**, while preserving legal source provenance, HSN hierarchy, effective date ranges, and rate schedules.

All data records are normalized into a unified **25-field schema**, supported by automated Python validation scripts (`scripts/validate_dataset.py`) enforcing 7 integrity rules.

---

##  Directory Architecture

| Path | Purpose & Description | Access & Provenance |
| :--- | :--- | :--- |
| `data/raw/` | Unmodified source files, raw CBIC notification PDFs, and raw regulatory scraped JSON files. | Read-Only Archive |
| `data/processed/` | Standardized, normalized production dataset (`hsn_master_normalized.json`) adhering to the 25-field schema. | Authoritative Engine Target |
| `data/validation/` | Validation log reports, constraint check runs, and audit error manifests. | Automated Pipeline Output |
| `data/samples/` | Synthetic/mock test products (`sample_test_products.json`) explicitly marked with `DEMO_SAMPLE` for UI testing. | Demo / UI Test Suite Only |

---

##  Standardized 25-Field Dataset Schema

Every record in `data/processed/hsn_master_normalized.json` and `data/samples/sample_test_products.json` contains the following exact 25 fields:

1. `product_name` — Trade/commercial item name
2. `product_description` — Detailed natural language description
3. `hsn_code` — String-encoded HSN code (preserves leading zeros, e.g. `"09011110"`)
4. `hsn_level` — Hierarchy indicator (`2-digit`, `4-digit`, `6-digit`, `8-digit`)
5. `chapter` — 2-digit Chapter code
6. `heading` — 4-digit Heading code
7. `subheading` — 6-digit Subheading code
8. `technical_description` — Official WCO/CBIC statutory description
9. `trade_description` — Commonly understood commercial description
10. `material` — Primary composition material
11. `category` — Broad taxonomy category
12. `gst_rate` — Total GST Rate percentage
13. `cgst_rate` — Central GST percentage
14. `sgst_rate` — State GST percentage
15. `igst_rate` — Integrated GST percentage
16. `cess_rate` — Compensation Cess percentage
17. `conditions` — Statutory conditions, exemptions, or threshold criteria
18. `source_document` — Title/Schedule entry of source notification
19. `source_url` — Direct URL link to official PDF/portal document
20. `notification_number` — Official CBIC notification identifier
21. `effective_from` — ISO date string (`YYYY-MM-DD`) when tax rate became active
22. `effective_to` — ISO date string (`YYYY-MM-DD`) or `null` if currently active
23. `retrieved_at` — Verification timestamp
24. `source_type` — Provenance class (`AUTHORITATIVE_CBIC` vs `DEMO_SAMPLE`)
25. `validation_status` — Verification state (`VERIFIED_AUTHORITATIVE`, `PROVISIONAL`, `DEPRECATED`)

---

## ️ Key Dataset Engineering Specifications

### 1. HSN Code String Normalization
- **Leading Zero Preservation**: HSN codes are stored strictly as `string` values to preserve leading zeros in Chapters 01–09 (e.g., `"09011110"` for raw coffee beans). Storing HSN codes as numbers would truncate `"09011110"` to `9011110`, causing critical lookup failures.
- **Hierarchy Mapping**:
  - `chapter` = `hsn_code[0:2]`
  - `heading` = `hsn_code[0:4]`
  - `subheading` = `hsn_code[0:6]`

### 2. Tax Rate Mathematical Consistency
- For intra-state transactions: `cgst_rate + sgst_rate == gst_rate`
- For inter-state transactions: `igst_rate == gst_rate`

### 3. Segregation of Demo & Production Data
- Authoritative records are tagged with `"source_type": "AUTHORITATIVE_CBIC"` and `"validation_status": "VERIFIED_AUTHORITATIVE"`.
- Test/Demo records are tagged with `"source_type": "DEMO_SAMPLE"` and `"validation_status": "PROVISIONAL"`.
- The RAG search and knowledge graph indexing engines load only `data/processed/` records for production inference.

---

##  Automated Dataset Validation Suite

The system includes `scripts/validate_dataset.py`, an automated integrity check runner verifying 7 core rules:

1. **Duplicate HSN Detection**: Detects multiple identical HSN codes across records.
2. **Invalid Format Detection**: Validates HSN string format (2, 4, 6, 8 digits) and level alignment.
3. **Missing Description**: Flags missing or overly short product/technical descriptions.
4. **Missing Source**: Verifies `source_document` and `source_url` presence.
5. **Inconsistent Rates**: Enforces `cgst_rate + sgst_rate == gst_rate` and `igst_rate == gst_rate`.
6. **Duplicate Source Records**: Detects identical product name + notification number pairs.
7. **Date Conflicts**: Ensures `effective_from <= effective_to` when `effective_to` is specified.

---

##  Dataset Validation Metrics

Run command:
```bash
python3 scripts/validate_dataset.py
```

### Validation Run Output:
```text
==========================================================
      SMART GST DATASET INTEGRITY VALIDATION RUNNER       
==========================================================

[+] Validating file: data/processed/hsn_master_normalized.json
  [*] Total records inspected: 3
  [*] Errors found: 0
  [*] Warnings found: 0
  [] FILE PASSED VALIDATION

[+] Validating file: data/samples/sample_test_products.json
  [*] Total records inspected: 3
  [*] Errors found: 0
  [*] Warnings found: 0
  [] FILE PASSED VALIDATION

----------------------------------------------------------
SUMMARY: Total Errors = 0, Total Warnings = 0
----------------------------------------------------------
```

---

##  Deliverables Summary

1. `data/raw/` (Raw provenance directory)
2. `data/processed/hsn_master_normalized.json` (Authoritative normalized dataset)
3. `data/validation/` (Validation logs & audit directory)
4. `data/samples/sample_test_products.json` (Isolated sample test dataset)
5. `docs/dataset/DATA_DICTIONARY.md` (Complete field specification document)
6. `docs/dataset/DATA_SOURCE_POLICY.md` (CBIC source provenance and acquisition policy)
7. `docs/dataset/DATA_VALIDATION_RULES.md` (Rulebook for integrity and rate checks)
8. `docs/dataset/DATASET_REPORT.md` (This Phase 3 completion report)
9. `scripts/validate_dataset.py` (Executable automated validator script)
