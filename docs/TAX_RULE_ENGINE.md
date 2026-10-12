# Deterministic Tax Rule Engine Specification

## 1. Overview & Architecture

The **GstTaxDomainEngine** ([`backend/app/services/evidence_validator.py`](backend/app/services/evidence_validator.py)) is the authoritative deterministic tax engine for the Smart GST System.

> **Deterministic Rule**: *Tax rates are NEVER calculated or decided by the LLM. The tax engine evaluates product attributes, supply state logic, transaction dates, and statutory conditions to calculate CGST, SGST, IGST, and Cess.*

---

## 2. Rule Resolution Engine Algorithm

```
Inputs:
  - Product Attributes (material, form, packaging, end-use)
  - HSN / SAC Code
  - Transaction Date
  - Seller State Code vs Buyer State Code
  - Transaction Value
  - Applicable Statutory Conditions

Algorithm:
  1. Filter active rules where code matches AND effective_from <= Transaction Date <= (effective_to OR current_date)
  2. If code_type == "SAC", set tax_type = "SERVICES"
  3. Evaluate conditions (e.g. value thresholds, unit container branding):
     - If apparel AND item_value <= ₹1,000  12% rate
     - If apparel AND item_value > ₹1,000  18% rate
  4. Evaluate Supply Type (Intra-State vs Inter-State):
     - If Seller State Code == Buyer State Code (Intra-State):
         CGST = GST_Rate / 2
         SGST = GST_Rate / 2
         IGST = 0
     - If Seller State Code != Buyer State Code (Inter-State):
         IGST = GST_Rate
         CGST = 0
         SGST = 0
  5. Compute Cess Rate (if applicable)
  6. Return Tax Breakdown Object + Source Citation Provenance
```

---

## 3. Invoice Calculation Determinism

For sales transaction invoices:
$$\text{Taxable Value} = (\text{Quantity} \times \text{Unit Price}) - \text{Valid Discount}$$

$$\text{Tax Amount} = \text{Taxable Value} \times \frac{\text{Applicable GST Rate}}{100}$$

$$\text{Grand Total} = \text{Taxable Value} + \text{Tax Amount}$$

Arithmetic is enforced deterministically by code with 2-decimal rounding.
