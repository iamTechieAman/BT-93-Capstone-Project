# GST Tax Invoice Automation & Rule 46 Compliance Specification

## 1. Executive Summary

The **Invoice Automation Module** ([`backend/app/api/v1/invoice.py`](backend/app/api/v1/invoice.py) & [`src/components/InvoiceModule.jsx`](src/components/InvoiceModule.jsx)) issues, validates, and renders official GST tax invoices compliant with **Rule 46 of CGST Rules, 2017**.

---

## 2. Core Safeguards & Hard Constraints

1. **Non-LLM Deterministic Tax Engine**: Tax calculations are performed strictly by exact arithmetic formulas in [`GstTaxDomainEngine`](backend/app/services/tax_domain_engine.py). LLM outputs are never used to compute tax amounts.
2. **Explicit Demo Data Marking**: All preset or simulated seller/buyer organizations are explicitly tagged with `[DEMO DATA]` badges to prevent misrepresentation of fake entities.
3. **11 Statutory Rule 46 Validations**:
   - Supplier GSTIN 15-char regex (`^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}Z[0-9A-Z]{1}$`)
   - Recipient GSTIN format validation
   - Unique Invoice Number presence
   - Invoice Date presence
   - Place of Supply alignment
   - Line items non-empty
   - Quantity $> 0$
   - Unit Price $\ge 0$
   - Discount $\le \text{Quantity} \times \text{Unit Price}$
   - Valid HSN/SAC code format
   - Tax amount exact arithmetic reconciliation (2 decimal place rounding)

---

## 3. Invoice Arithmetic Formulas

$$\text{Taxable Value} = (\text{Quantity} \times \text{Unit Price}) - \text{Discount}$$

$$\text{If Intra-State } (\text{Supplier State} = \text{Place of Supply}):$$
$$\text{CGST} = \text{Taxable Value} \times \frac{\text{GST Rate}}{2} \%, \quad \text{SGST} = \text{Taxable Value} \times \frac{\text{GST Rate}}{2} \%, \quad \text{IGST} = 0$$

$$\text{If Inter-State } (\text{Supplier State} \neq \text{Place of Supply}):$$
$$\text{CGST} = 0, \quad \text{SGST} = 0, \quad \text{IGST} = \text{Taxable Value} \times \text{GST Rate} \%$$

$$\text{Cess} = \text{Taxable Value} \times \text{Cess Rate} \%$$

$$\text{Grand Total} = \text{Taxable Value} + \text{CGST} + \text{SGST} + \text{IGST} + \text{Cess}$$

---

## 4. UI Capabilities

- **Product Master & One-Click Verification Sync**: Import verified HSN items directly from verification studio.
- **Multi-Item Sales Table**: Edit description, HSN/SAC, quantity, rate, discount, and GST rate dynamically.
- **Rule 46 Tax Invoice Preview**: Official printable tax invoice format.
- **Browser Print / PDF Export**: Built-in print trigger (`window.print()`).
