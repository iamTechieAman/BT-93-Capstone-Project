# Tax Data Governance Architecture

## 1. Governance Principles & Strict Rules

The **Smart GST System** enforces rigorous data governance rules to guarantee the integrity of all indirect tax rules, HSN/SAC classification codes, statutory GST rates, and legal source citations.

> **Data Integrity Principle**: *Never invent or hallucinate HSN codes, SAC codes, or GST tax rates. Every tax rule MUST have verified source provenance and effective date ranges.*

---

## 2. Tax Rule Record Schema Specification

All tax rule entries are structured in the database schema ([`backend/app/models/database_models.py`](backend/app/models/database_models.py)) with the following canonical fields:

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `code` | `VARCHAR(10)` | Not Null | 8-digit HSN code (Goods) or 6-digit SAC code (Services) |
| `code_type` | `VARCHAR(10)` | Enum (`HSN`, `SAC`) | Distinguishes Goods classification vs Service classification |
| `description` | `TEXT` | Not Null | Official statutory description |
| `chapter` | `VARCHAR(4)` | Not Null | 2-digit Chapter code (01-99 for HSN, 99 for SAC) |
| `heading` | `VARCHAR(6)` | Not Null | 4-digit Heading code |
| `subheading` | `VARCHAR(8)` | Optional | Subheading tariff level |
| `tariff_item` | `VARCHAR(10)` | Optional | 8-digit Tariff item level |
| `gst_rate` | `NUMERIC(5,2)` | Not Null | Total effective GST percentage (e.g. 18.00) |
| `cgst_rate` | `NUMERIC(5,2)` | Not Null | Central GST percentage (50% of GST rate for Intra-State) |
| `sgst_rate` | `NUMERIC(5,2)` | Not Null | State GST percentage (50% of GST rate for Intra-State) |
| `igst_rate` | `NUMERIC(5,2)` | Not Null | Integrated GST percentage (100% of GST rate for Inter-State) |
| `cess_rate` | `NUMERIC(5,2)` | Default `0.00` | Compensation Cess percentage |
| `conditions` | `TEXT` | Optional | Specific statutory conditions (e.g. unit container, brand name, value thresholds) |
| `exceptions` | `TEXT` | Optional | Explicit exclusions |
| `effective_from` | `DATE` | Not Null | Effective start date of notification |
| `effective_to` | `DATE` | Optional | Effective end date (null if current) |
| `source_name` | `VARCHAR(255)` | Not Null | Publisher name (e.g. CBIC) |
| `source_url` | `VARCHAR(500)` | Not Null | Verified URL to PDF/Gazette notification |
| `source_document` | `VARCHAR(255)` | Not Null | Document title or notification number |
| `source_page` | `VARCHAR(50)` | Optional | Page / Schedule entry reference |
| `notification_number` | `VARCHAR(100)` | Not Null | Gazette Notification number (e.g. `1/2017-Central Tax (Rate)`) |
| `notification_date` | `DATE` | Not Null | Notification issuance date |
| `retrieved_at` | `TIMESTAMP` | Not Null | System ingestion timestamp |
| `verification_status` | `VARCHAR(50)` | Enum | `VERIFIED`, `PARTIALLY_VERIFIED`, `REQUIRES_REVIEW` |
| `last_verified_at` | `TIMESTAMP` | Not Null | Timestamp of last legal review |

---

## 3. Effective Date & Historical Versioning Policy

When CBIC issues a new notification modifying a tax rate or condition:
1. The historical rule's `effective_to` date is set to the day before the new notification takes effect.
2. A new version of the rule is inserted with `effective_from` set to the new effective date and `effective_to` set to `null`.
3. Historical rules are NEVER silently overwritten or deleted, preserving retro-active tax auditability.
