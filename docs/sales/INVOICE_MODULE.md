# Statutory Tax Invoice Module Documentation

## 1. System Overview & Domain Constraint

The **Statutory Tax Invoice Module** generates GST-compliant tax invoices, handles intra-state vs inter-state supply tax splits, and performs automated mathematical validation.

### ️ Critical Domain Layer Constraint
> **Mandatory Rule**: *Do not duplicate GST rules inside invoice code. Invoice logic must consume validated GST/HSN information from the domain layer.*

All tax calculation logic is encapsulated within the domain layer ([`GstTaxDomainEngine`](backend/app/services/tax_domain_engine.py)). Invoice creation and validation methods invoke the domain calculation engine rather than hardcoding tax rules.

---

## 2. Tax Calculation Mathematical Rules

### 1. Automatic Taxable Value Calculation
$$\text{Taxable Value} = \text{round}(\text{Quantity} \times \text{Unit Price}, 2)$$

### 2. CGST / SGST / IGST Tax Split

- **Intra-State Supply** (`Supplier GSTIN State == Place of Supply State`):
  $$\text{CGST Amount} = \text{round}\left(\text{Taxable Value} \times \frac{\text{GST Rate} / 2.0}{100.0}, 2\right)$$
  $$\text{SGST Amount} = \text{round}\left(\text{Taxable Value} \times \frac{\text{GST Rate} / 2.0}{100.0}, 2\right)$$
  $$\text{IGST Amount} = 0.0$$

- **Inter-State Supply** (`Supplier GSTIN State != Place of Supply State`):
  $$\text{IGST Amount} = \text{round}\left(\text{Taxable Value} \times \frac{\text{GST Rate}}{100.0}, 2\right)$$
  $$\text{CGST Amount} = 0.0, \quad \text{SGST Amount} = 0.0$$

### 3. Grand Total Aggregation
$$\text{Grand Total} = \sum \text{Taxable Values} + \sum \text{CGST} + \sum \text{SGST} + \sum \text{IGST} + \sum \text{Cess}$$

---

## 3. REST API Endpoints

- `POST /api/v1/invoices`: Create statutory tax invoice from confirmed sale.
- `GET /api/v1/invoices/{id}`: Retrieve invoice record.
- `POST /api/v1/invoice/validate`: Validate invoice mathematical accuracy and GSTIN state alignment.
