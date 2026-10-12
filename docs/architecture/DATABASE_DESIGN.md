# Database Architecture & Schema Specification

## Executive Summary

The **Smart GST Verification & Sales System** uses PostgreSQL 14+ as its core relational data store. The database schema is designed for production tax compliance, auditability, deterministic tax calculations, and multi-agent AI verification logging.

The database consists of **15 normalized relational tables** with strict UUID primary keys, foreign key constraints, mathematical check constraints for GST tax splits, effective date handling, source provenance tracking, and an append-only audit trail.

---

## ️ Relational Schema Overview (15 Tables)

### 1. User & Identity Domain
- **`users`**: System user accounts, credentials, and RBAC roles (`ADMIN`, `USER`, `AUDITOR`, `TAX_EXPERT`). Includes audit fields for record creation and updates.

### 2. Regulatory & Provenance Domain
- **`sources`**: Authoritative tax sources (CBIC Notifications, State Tax Gazette entries, Statutory Circulars). Stores document URLs and retrieval timestamps.
- **`notifications`**: Official CBIC/State notifications issuing tax rate amendments or exemption schedules, with effective date range support (`effective_from` to `effective_to`).

### 3. HSN & GST Rule Engine Domain
- **`hsn_codes`**: Harmonized System of Nomenclature master directory (2, 4, 6, and 8-digit levels). Stores WCO technical descriptions and trade descriptions. Preserves leading zeros.
- **`gst_rates`**: Historical and current GST tax rate schedules (`gst_rate`, `cgst_rate`, `sgst_rate`, `igst_rate`, `cess_rate`) mapped to specific HSN codes and notifications. Includes check constraints verifying `cgst_rate + sgst_rate == gst_rate`.
- **`gst_rules`**: Conditional statutory rules, exemptions, thresholds, and exception criteria linked to HSN codes and notifications.

### 4. Product Catalog Domain
- **`products`**: Manufacturing product master items linked to verified HSN codes, material composition, categories, and standard unit prices.

### 5. Multi-Agent AI Verification Domain
- **`verification_requests`**: Audit log of natural language product description verification prompts submitted by users or API consumers.
- **`verification_results`**: AI decision outputs containing recommended HSN code, verified tax rates, confidence score (75%–99%), chain-of-thought JSON, and reasoning summaries.
- **`retrieval_chunks`**: Fine-grained RAG context snippets and vector search hits retrieved during verification, with relevance scores and source references.

### 6. Sales & Invoicing Domain
- **`sales`**: Sales orders generated in the ERP workflow with customer details, order dates, and status (`DRAFT`, `CONFIRMED`, `CANCELLED`).
- **`sale_items`**: Line items within a sale order, referencing product IDs, HSN codes, taxable values, and applied GST rates.
- **`invoices`**: GST-compliant tax invoices linked to sales orders. Stores place of supply, supplier/customer GSTINs, aggregate taxable values, CGST/SGST/IGST breakdown, and validation status (`is_validated`).
- **`invoice_items`**: Detailed invoice line items with calculated tax amounts (`cgst_amount`, `sgst_amount`, `igst_amount`, `cess_amount`).

### 7. Audit & Compliance Domain
- **`audit_logs`**: System-wide audit log recording user actions, IP addresses, target entities, and JSON diffs for regulatory compliance.

---

##  Table Definitions & Constraints

### 1. `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY, DEFAULT `uuid_generate_v4()` | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User login email |
| `full_name` | VARCHAR(255) | NOT NULL | User display name |
| `hashed_password`| VARCHAR(255) | NOT NULL | Password hash |
| `role` | VARCHAR(50) | NOT NULL, CHECK role IN (...) | RBAC Role |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account active flag |
| `created_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMPTZ | DEFAULT CURRENT_TIMESTAMP | Record update time |
| `created_by` | UUID | FK -> `users.id` | Creator user |
| `updated_by` | UUID | FK -> `users.id` | Updater user |

### 2. `gst_rates`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique rate schedule ID |
| `hsn_code_id` | UUID | FK -> `hsn_codes.id` (CASCADE) | Associated HSN code |
| `notification_id`| UUID | FK -> `notifications.id` (RESTRICT)| Issuing CBIC notification |
| `gst_rate` | NUMERIC(5,2)| NOT NULL | Total GST percentage |
| `cgst_rate` | NUMERIC(5,2)| NOT NULL | Central GST percentage |
| `sgst_rate` | NUMERIC(5,2)| NOT NULL | State GST percentage |
| `igst_rate` | NUMERIC(5,2)| NOT NULL | Integrated GST percentage |
| `cess_rate` | NUMERIC(5,2)| DEFAULT 0.00 | Compensation Cess |
| `effective_from` | DATE | NOT NULL | Rate active start date |
| `effective_to` | DATE | NULLABLE | Rate active end date |

**Check Constraints**:
- `check_gst_rate_math`: `(cgst_rate + sgst_rate = gst_rate) AND (igst_rate = gst_rate)`
- `check_gst_rate_dates`: `effective_to IS NULL OR effective_from <= effective_to`

---

##  Indexing Strategy

1. **B-Tree Indexes on Foreign Keys**:
   - `idx_gst_rates_hsn` ON `gst_rates(hsn_code_id)`
   - `idx_products_hsn` ON `products(hsn_code_id)`
   - `idx_sale_items_sale` ON `sale_items(sale_id)`
   - `idx_invoice_items_invoice` ON `invoice_items(invoice_id)`
2. **Natural Key & Lookups**:
   - `idx_users_email` ON `users(email)`
   - `idx_hsn_code` ON `hsn_codes(hsn_code)`
   - `idx_hsn_chapter` ON `hsn_codes(chapter)`
   - `idx_notifications_number` ON `notifications(notification_number)`
   - `idx_invoices_number` ON `invoices(invoice_number)`
3. **Temporal Range Queries**:
   - `idx_notifications_effective` ON `notifications(effective_from, effective_to)`
   - `idx_gst_rates_effective` ON `gst_rates(effective_from, effective_to)`
   - `idx_audit_logs_timestamp` ON `audit_logs(timestamp)`

---

## ️ Data Provenance & Tax Rule Safeguards

- **No Frontend Business Rules**: All tax rate calculations and HSN lookup rules reside within backend service layers and SQL schemas.
- **Traceability**: Every `gst_rate` and `gst_rule` explicitly references a valid `notification_id` and underlying `source_id`.
- **Effective Date Range Queries**: Rate queries evaluate `WHERE effective_from <= :target_date AND (effective_to IS NULL OR effective_to >= :target_date)`.
