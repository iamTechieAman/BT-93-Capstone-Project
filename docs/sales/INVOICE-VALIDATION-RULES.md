# Statutory GST Invoice Validation Rules & Specification

## 1. Overview
Before invoice finalization, every line item on a GST invoice must be validated deterministically against statutory CGST/IGST tariff rules, CBIC notifications, and place of supply logic. This document defines the 10 statutory validation dimensions implemented by the `GstTaxDomainEngine` and enforced by `InvoiceService`.

---

## 2. The 10 Statutory Line Item Validation Dimensions

| # | Validation Rule | Description & Criteria | Enforcement State |
|---|---|---|---|
| **1** | **Code Existence** | The HSN or SAC tariff code must exist in official CBIC tariff schedules and contain at least 2 digits (e.g. `42031010` for HSN, `998311` for SAC). | Critical Failure |
| **2** | **Code Type Correctness** | Goods (HSN, Chapters 01–98) vs Services (SAC, Chapter 99). Mismatched code labels are rejected. | Critical Failure |
| **3** | **Description Compatibility** | Line item description must be present and non-empty (>= 2 characters) matching official tariff nomenclature. | Critical Failure |
| **4** | **Statutory Rate Existence** | GST tax rate must match statutory schedules: `0.0%`, `0.25%`, `3.0%`, `5.0%`, `12.0%`, `18.0%`, `28.0%`. Non-statutory custom rates are strictly forbidden. | Critical Failure |
| **5** | **Rate Effective Period** | The tax rate rule must be effective on the invoice date (`effective_from <= invoice_date <= effective_to`). Stale or expired tax rules block finalization. | Critical Failure |
| **6** | **Source Provenance** | Every tariff rate and code must originate from an authoritative statutory document (CBIC Notification, Circular, or Advance Ruling). | Critical Failure |
| **7** | **Required Conditions** | Specific conditions (e.g., maximum retail price limits, composition scheme exemptions) must be satisfied. | Verification State |
| **8** | **Supply Type Validity** | Supply type must correctly distinguish Intra-state (CGST + SGST) vs Inter-state (IGST) based on seller state vs place of supply state. | Critical Failure |
| **9** | **State Logic Validity** | Valid 2-digit state codes (e.g. `07` Delhi, `27` Maharashtra) must be present for both supplier and place of supply. | Critical Failure |
| **10** | **Tax Arithmetic Validity** | Quantity must be positive (`qty > 0`), unit price non-negative (`price >= 0`), discount cannot exceed gross value (`discount <= gross`), and computed tax must match statutory formulas. | Critical Failure |

---

## 3. Mandatory Line Display Attributes

Every line item displayed on the invoice UI and payload contains:
1. **HSN/SAC Code**
2. **Code Type** (`HSN` vs `SAC`)
3. **GST Rate** (%)
4. **Taxable Value** (₹)
5. **CGST Amount** (₹)
6. **SGST Amount** (₹)
7. **IGST Amount** (₹)
8. **Compensation Cess** (₹)
9. **Line Total** (₹)
10. **Validation Status** (`VALIDATED` vs `FAILED` with exact error reasons)

---

## 4. Finalization Blocking Matrix

Invoice finalization (printing, issuing, PDF generation, or GSTR-1 saving) is **strictly blocked** if any of the following conditions occur:

```
[Invoice Finalization Attempt]
       │
       ├── Negative or zero quantity? ───────────► [BLOCK FINALIZATION]
       ├── Non-statutory GST rate? ──────────────► [BLOCK FINALIZATION]
       ├── Invalid or missing HSN/SAC code? ────► [BLOCK FINALIZATION]
       ├── Code type mismatch (e.g. HSN 9983)? ──► [BLOCK FINALIZATION]
       ├── Stale/expired tax rule on date? ──────► [BLOCK FINALIZATION]
       └── Missing source document provenance? ──► [BLOCK FINALIZATION]
       │
       └── All 10 Checks Passed ──────────────────► [ISSUE RULE 46 TAX INVOICE]
```

---

## 5. Audit & Compliance Trail
Whenever line item validation executes, detailed audit logs record the request timestamp, user ID, line item validations, and execution outcome in `audit_logs` for statutory compliance review.
