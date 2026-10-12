# Invoice Validation & Rule 46 Compliance Specification

## 1. Overview & Statutory Framework

The **Sales & Invoice Module** ([`src/components/InvoiceModule.jsx`](src/components/InvoiceModule.jsx)) generates statutory tax invoices compliant with **Rule 46 of the CGST Rules, 2017**.

---

## 2. Line Item & Invoice Validation Checklist

Before an invoice can be finalized or exported, the validation engine checks:

| Validation Step | Validation Rule | Action on Failure |
| :--- | :--- | :--- |
| **1. Code Validity** | HSN/SAC code must exist in canonical database | Block invoice finalization; flag invalid line item |
| **2. Code Type Matching** | Goods items must have `code_type = HSN`; Service items must have `code_type = SAC` | Correct code type label |
| **3. Rate Verification** | Tax rate must match active statutory rule schedule | Reconcile with statutory GST rate |
| **4. Supply State Logic** | Intra-State (Supplier State == Recipient State)  CGST + SGST; Inter-State  IGST | Adjust tax breakdown dynamically |
| **5. Arithmetic Accuracy** | Taxable Value = $(\text{Qty} \times \text{Rate}) - \text{Discount}$; Tax = $\text{Taxable} \times \text{GST\%}$ | Recalculate deterministically |
| **6. GSTIN Format** | Supplier and Buyer GSTINs must match regex `^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z0-9]{1}Z[A-Z0-9]{1}$` | Display format validation warning |

---

## 3. Demo Data Labeling Standard

All pre-populated default supplier and recipient organizations (e.g. *Apex Luxury Traders Pvt Ltd*) are explicitly labeled with **"DEMO DATA / TEST FIXTURE"** badges in the UI to prevent mistaking test data for actual legal advice.
