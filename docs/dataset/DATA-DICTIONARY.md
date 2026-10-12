# Authoritative GST & HSN Data Dictionary

## 1. Overview & Data Schema Specification

This Data Dictionary defines the canonical 27-field schema used across all raw, processed, validation, and sample dataset stores in the **Smart GST Verifier & Compliance Engine**.

---

## 2. Field Specifications Table

| Field Name | Type | Constraint | Description / Verification Rule |
| :--- | :--- | :--- | :--- |
| `code` | `VARCHAR(10)` | Not Null | 8-digit HSN code (Goods) or 6-digit SAC code (Services) |
| `code_type` | `VARCHAR(10)` | Enum (`HSN`, `SAC`) | Distinguishes Goods tariff code vs Service accounting code |
| `description` | `TEXT` | Not Null | Official statutory CBIC description |
| `chapter` | `VARCHAR(4)` | Not Null | 2-digit Chapter code (01-99 for HSN, 99 for SAC) |
| `heading` | `VARCHAR(6)` | Not Null | 4-digit Heading tariff level |
| `subheading` | `VARCHAR(8)` | Optional | 6-digit Subheading level |
| `tariff_item` | `VARCHAR(10)` | Optional | 8-digit Tariff item level |
| `category` | `VARCHAR(100)` | Not Null | High-level commodity or service group |
| `material` | `VARCHAR(100)` | Optional | Primary material composition (e.g. Bovine Leather, Silicon) |
| `gst_rate` | `NUMERIC(5,2)` | Not Null | Total effective statutory GST percentage |
| `cgst_rate` | `NUMERIC(5,2)` | Not Null | Central GST percentage (50% of GST rate for Intra-State) |
| `sgst_rate` | `NUMERIC(5,2)` | Not Null | State GST percentage (50% of GST rate for Intra-State) |
| `igst_rate` | `NUMERIC(5,2)` | Not Null | Integrated GST percentage (100% of GST rate for Inter-State) |
| `cess_rate` | `NUMERIC(5,2)` | Default `0.00` | Compensation Cess percentage |
| `conditions` | `TEXT` | Optional | Specific statutory conditions (e.g. unit container branding) |
| `exceptions` | `TEXT` | Optional | Explicit exclusions |
| `effective_from` | `DATE` | Not Null | Effective start date of notification |
| `effective_to` | `DATE` | Optional | Effective end date (`null` if active) |
| `source_name` | `VARCHAR(255)` | Not Null | Publishing authority (e.g. `CBIC`) |
| `source_url` | `VARCHAR(500)` | Not Null | Direct HTTPS link to statutory notification PDF/Gazette |
| `source_document` | `VARCHAR(255)` | Not Null | Notification title or document identifier |
| `source_page` | `VARCHAR(50)` | Optional | Page or entry schedule reference |
| `notification_number` | `VARCHAR(100)` | Not Null | Official notification number (e.g. `1/2017-Central Tax (Rate)`) |
| `notification_date` | `DATE` | Not Null | Gazette notification publication date |
| `retrieved_at` | `TIMESTAMP` | Not Null | Ingestion timestamp |
| `verification_status` | `VARCHAR(50)` | Enum | `VERIFIED_AUTHORITATIVE`, `PROVISIONAL`, `DEPRECATED` |
| `last_verified_at` | `TIMESTAMP` | Not Null | Timestamp of last manual or automated verification pass |

---

## 3. Data Store Directory Layout

- `data/raw/`: Original un-processed CBIC notification schedules and JSON downloads.
- `data/processed/`: Standardized, normalized canonical dataset files (`hsn_master_normalized.json`).
- `data/validation/`: Validation schemas and automated audit rule definitions.
- `data/samples/`: Explicitly badged `DEMO DATA` sample fixtures (`sample_test_products.json`).
