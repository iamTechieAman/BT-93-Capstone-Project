# Entity-Relationship (ER) Diagram

## Executive Overview

The following Mermaid ER diagram illustrates the complete 15-table relational schema for the **Smart GST Verification & Sales System**, showing entity attributes, primary keys, foreign keys, cardinality, and domain relationships.

---

##  Complete System ER Diagram

```mermaid
erDiagram

    USERS ||--o{ SOURCES : "creates/updates"
    USERS ||--o{ NOTIFICATIONS : "creates/updates"
    USERS ||--o{ HSN_CODES : "creates/updates"
    USERS ||--o{ PRODUCTS : "creates/updates"
    USERS ||--o{ SALES : "creates/updates"
    USERS ||--o{ INVOICES : "creates/updates"
    USERS ||--o{ VERIFICATION_REQUESTS : "submits"
    USERS ||--o{ AUDIT_LOGS : "triggers"

    SOURCES ||--o{ NOTIFICATIONS : "issues"
    SOURCES ||--o{ RETRIEVAL_CHUNKS : "provides context"

    NOTIFICATIONS ||--o{ GST_RATES : "defines"
    NOTIFICATIONS ||--o{ GST_RULES : "specifies"

    HSN_CODES ||--o{ GST_RATES : "has rates"
    HSN_CODES ||--o{ GST_RULES : "has rules"
    HSN_CODES ||--o{ PRODUCTS : "classifies"
    HSN_CODES ||--o{ VERIFICATION_RESULTS : "recommended in"
    HSN_CODES ||--o{ SALE_ITEMS : "applied to"

    PRODUCTS ||--o{ SALE_ITEMS : "included in"

    VERIFICATION_REQUESTS ||--|| VERIFICATION_RESULTS : "produces"
    VERIFICATION_RESULTS ||--o{ RETRIEVAL_CHUNKS : "cites"

    SALES ||--o{ SALE_ITEMS : "contains"
    SALES ||--|| INVOICES : "generates"

    INVOICES ||--o{ INVOICE_ITEMS : "contains"

    USERS {
        uuid id PK
        string email UK
        string full_name
        string role
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    SOURCES {
        uuid id PK
        string title
        string source_type
        string publisher
        text document_url
        datetime retrieved_at
    }

    NOTIFICATIONS {
        uuid id PK
        uuid source_id FK
        string notification_number UK
        string title
        date effective_from
        date effective_to
    }

    HSN_CODES {
        uuid id PK
        string hsn_code UK
        string hsn_level
        string chapter
        string heading
        string subheading
        text technical_description
        string category
    }

    GST_RATES {
        uuid id PK
        uuid hsn_code_id FK
        uuid notification_id FK
        decimal gst_rate
        decimal cgst_rate
        decimal sgst_rate
        decimal igst_rate
        decimal cess_rate
        date effective_from
        date effective_to
    }

    GST_RULES {
        uuid id PK
        uuid hsn_code_id FK
        uuid notification_id FK
        string rule_name
        text conditions
        text exceptions
        date effective_from
        date effective_to
    }

    PRODUCTS {
        uuid id PK
        string product_name
        text product_description
        string material
        string category
        uuid hsn_code_id FK
        decimal unit_price
        boolean is_active
    }

    VERIFICATION_REQUESTS {
        uuid id PK
        uuid user_id FK
        string product_name
        text product_description
        string declared_hsn
        string status
        datetime created_at
    }

    VERIFICATION_RESULTS {
        uuid id PK
        uuid request_id FK,UK
        uuid recommended_hsn_id FK
        decimal verified_gst_rate
        decimal confidence_score
        text reasoning_summary
        jsonb chain_of_thought
        string validation_status
    }

    RETRIEVAL_CHUNKS {
        uuid id PK
        uuid verification_result_id FK
        uuid source_id FK
        text chunk_text
        decimal relevance_score
        jsonb chunk_metadata
    }

    SALES {
        uuid id PK
        string sale_number UK
        string customer_name
        string customer_gstin
        date sale_date
        string status
        decimal total_amount
    }

    SALE_ITEMS {
        uuid id PK
        sale_id uuid FK
        product_id uuid FK
        hsn_code_id uuid FK
        decimal quantity
        decimal unit_price
        decimal taxable_value
        decimal gst_rate
    }

    INVOICES {
        uuid id PK
        uuid sale_id FK,UK
        string invoice_number UK
        date invoice_date
        string place_of_supply
        string supplier_gstin
        string customer_gstin
        decimal total_taxable_value
        decimal total_cgst
        decimal total_sgst
        decimal total_igst
        decimal total_cess
        decimal grand_total
        boolean is_validated
    }

    INVOICE_ITEMS {
        uuid id PK
        uuid invoice_id FK
        string product_name
        string hsn_code
        decimal quantity
        decimal unit_price
        decimal taxable_value
        decimal gst_rate
        decimal cgst_amount
        decimal sgst_amount
        decimal igst_amount
        decimal cess_amount
        decimal item_total
    }

    AUDIT_LOGS {
        uuid id PK
        uuid user_id FK
        string action
        string entity_name
        uuid entity_id
        string ip_address
        jsonb changes_json
        datetime timestamp
    }
```

---

##  Key Domain Relationship Highlights

1. **Tax Rates & Legal Provenance**:
   - `NOTIFICATIONS` links `SOURCES` to `GST_RATES` and `GST_RULES`.
   - Every tax rate applied to an HSN code is directly traceable to an official legal notification.

2. **Multi-Agent Verification & Evidence Trail**:
   - A `VERIFICATION_REQUEST` produces exactly one `VERIFICATION_RESULT`.
   - A `VERIFICATION_RESULT` cites one or more `RETRIEVAL_CHUNKS` linked back to authoritative `SOURCES`.

3. **Sales to Invoicing Pipeline**:
   - A `SALE` contains multiple `SALE_ITEMS`.
   - A `SALE` generates exactly one validated `INVOICE`.
   - An `INVOICE` contains detailed `INVOICE_ITEMS` with calculated CGST, SGST, IGST, and Cess tax amounts.
