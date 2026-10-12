# DATA_VALIDATION_RULES.md — Dataset Integrity & Validation Specification

**Project**: Smart GST Verification and Manufacturing Sales Automation System  
**Document Identifier**: DVR-GST-2026-V2.4  
**Date**: October 8, 2026  

---

## 1. Automated Validation Checks

Every dataset update must pass the automated validation script (`scripts/validate_dataset.py`) enforcing 7 integrity rules:

### Rule 1: Duplicate HSN Detection
- **Check**: No two records with the same `hsn_code` and overlapping `effective_from` / `effective_to` dates shall exist.

### Rule 2: HSN Format Integrity
- **Check**: `hsn_code` must strictly match 2, 4, 6, or 8 numeric digits (`^\d{2,8}$`). Leading zeroes must be preserved (e.g. HSN `0901`).

### Rule 3: Description Completeness
- **Check**: `product_name`, `product_description`, and `technical_description` must not be null or empty.

### Rule 4: Source Provenance Mandatory Check
- **Check**: `source_document`, `source_url`, and `notification_number` must be populated.

### Rule 5: Tax Rate Consistency
- **Check**: `cgst_rate + sgst_rate` must equal `gst_rate`. `igst_rate` must equal `gst_rate`.

### Rule 6: Date Conflict Check
- **Check**: `effective_from` must be a valid date <= `effective_to` (if `effective_to` is present).

### Rule 7: Source Type Segregation
- **Check**: `source_type` must be either `AUTHORITATIVE_CBIC` or `DEMO_SAMPLE`. Demo samples must be stored separately in `data/samples/`.
