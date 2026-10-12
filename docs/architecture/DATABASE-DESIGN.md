# Database Architecture & Relational Design Specification

## 1. Executive Summary & Design Principles

The **Smart GST System** database architecture is implemented in PostgreSQL 16 (with `pgvector` support) using SQLAlchemy ORM ([`backend/app/models/database_models.py`](backend/app/models/database_models.py)).

### Core Database Principles
1. **Relational Integrity**: Foreign key constraints with explicit `ondelete` actions (`CASCADE`, `RESTRICT`, `SET NULL`).
2. **Indexing Strategy**: B-Tree indexes on HSN/SAC codes, notification numbers, foreign key columns, and timestamps.
3. **Audit Provenance**: Every entity table records `created_at`, `updated_at`, `created_by`, and `updated_by`.
4. **Historical Rule Versioning**: `gst_rule_versions` table preserves version history without overwriting past entries.

---

## 2. Relational Table Schema Catalog

The system defines 17 core relational tables:

| Table Name | Primary Key | Foreign Keys | Key Purpose |
| :--- | :--- | :--- | :--- |
| `users` | `id (UUID)` | Self-referential `created_by` | User accounts, roles (`ADMIN`, `COMPLIANCE_OFFICER`, `USER`). |
| `sources` | `id (UUID)` | `created_by`  `users.id` | Authoritative CBIC source publishers. |
| `notifications` | `id (UUID)` | `source_id`  `sources.id` | Official CBIC tax notifications with date ranges. |
| `hsn_codes` | `id (UUID)` | `created_by`  `users.id` | Canonical 8-digit HSN codes for Goods. |
| `sac_codes` | `id (UUID)` | `created_by`  `users.id` | Canonical 6-digit SAC codes for Services. |
| `gst_rates` | `id (UUID)` | `hsn_code_id`, `notification_id` | Statutory tax rate schedules (CGST, SGST, IGST, Cess). |
| `gst_rules` | `id (UUID)` | `hsn_code_id`, `notification_id` | Tax conditions and exceptions. |
| `gst_rule_versions` | `id (UUID)` | `rule_id`  `gst_rules.id` | Historical version history for tax rules. |
| `products` | `id (UUID)` | `hsn_code_id`  `hsn_codes.id` | Product Master catalog. |
| `verification_requests` | `id (UUID)` | `user_id`  `users.id` | Raw trade query verification submissions. |
| `verification_results` | `id (UUID)` | `request_id`, `recommended_hsn_id` | Output classification, scores, and CoT summaries. |
| `retrieval_chunks` | `id (UUID)` | `verification_result_id`, `source_id` | Retrieved RAG document chunks for verification evidence. |
| `sales` | `id (UUID)` | `created_by`  `users.id` | Commercial sales transactions. |
| `sale_items` | `id (UUID)` | `sale_id`, `product_id`, `hsn_code_id` | Line items attached to sales transactions. |
| `invoices` | `id (UUID)` | `sale_id`  `sales.id` | Rule 46 compliant GST tax invoices. |
| `invoice_items` | `id (UUID)` | `invoice_id`  `invoices.id` | Line item tax calculations (CGST, SGST, IGST, Cess). |
| `audit_logs` | `id (UUID)` | `user_id`  `users.id` | Immutable audit trail for dataset mutations. |
