# Smart GST System — Entity Relationship (ER) Diagram

## 1. Overview & Legend

The Entity Relationship (ER) diagram below models the complete 17-entity database schema for the Smart GST System, covering:
- **Authentication & Governance**: `users`, `audit_logs`
- **Statutory Master Data**: `sources`, `notifications`, `hsn_codes`, `sac_codes`, `gst_rates`, `gst_rules`, `gst_rule_versions`
- **Product Catalog & Sales**: `products`, `sales`, `sale_items`, `invoices`, `invoice_items`
- **AI Verification & RAG**: `verification_requests`, `verification_results`, `retrieval_chunks`

---

## 2. Mermaid Entity-Relationship Diagram

```mermaid
erDiagram
    users ||--o{ sources : "creates"
    users ||--o{ notifications : "creates"
    users ||--o{ hsn_codes : "creates"
    users ||--o{ products : "creates"
    users ||--o{ verification_requests : "initiates"
    users ||--o{ sales : "creates"
    users ||--o{ invoices : "generates"
    users ||--o{ audit_logs : "triggers"

    sources ||--o{ notifications : "publishes"
    sources ||--o{ retrieval_chunks : "provides_evidence"

    notifications ||--o{ gst_rates : "notifies"
    notifications ||--o{ gst_rules : "establishes"

    hsn_codes ||--o{ gst_rates : "has_rates"
    hsn_codes ||--o{ gst_rules : "governed_by"
    hsn_codes ||--o{ products : "classifies"
    hsn_codes ||--o{ verification_results : "recommended_in"

    gst_rules ||--o{ gst_rule_versions : "has_versions"

    products ||--o{ sale_items : "sold_as"

    verification_requests ||--|| verification_results : "produces"
    verification_results ||--o{ retrieval_chunks : "supported_by"

    sales ||--o{ sale_items : "contains"
    sales ||--|| invoices : "billed_as"

    invoices ||--o{ invoice_items : "itemizes"

    users {
        string id PK
        string email UK
        string full_name
        string role
        boolean is_active
        datetime created_at
    }

    sources {
        string id PK
        string title
        string source_type
        string publisher
        string document_url
    }

    notifications {
        string id PK
        string source_id FK
        string notification_number UK
        date effective_from
        date effective_to
    }

    hsn_codes {
        string id PK
        string hsn_code UK
        string hsn_level
        string chapter
        string category
    }

    sac_codes {
        string id PK
        string sac_code UK
        string chapter
        string description
    }

    gst_rates {
        string id PK
        string hsn_code_id FK
        string notification_id FK
        float gst_rate
        float cgst_rate
        float sgst_rate
        float igst_rate
    }

    gst_rules {
        string id PK
        string hsn_code_id FK
        string notification_id FK
        string rule_name
        text conditions
    }

    gst_rule_versions {
        string id PK
        string rule_id FK
        integer version_number
        text conditions
    }

    products {
        string id PK
        string product_name
        string hsn_code_id FK
        float unit_price
    }

    verification_requests {
        string id PK
        string user_id FK
        string product_name
        string status
    }

    verification_results {
        string id PK
        string request_id FK
        string recommended_hsn_id FK
        float verified_gst_rate
        float confidence_score
    }

    retrieval_chunks {
        string id PK
        string verification_result_id FK
        string source_id FK
        float relevance_score
    }

    sales {
        string id PK
        string sale_number UK
        string customer_name
        float total_amount
    }

    sale_items {
        string id PK
        string sale_id FK
        string product_id FK
        float quantity
        float taxable_value
    }

    invoices {
        string id PK
        string sale_id FK
        string invoice_number UK
        float grand_total
        boolean is_validated
    }

    invoice_items {
        string id PK
        string invoice_id FK
        string product_name
        float item_total
    }

    audit_logs {
        string id PK
        string user_id FK
        string action
        string entity_name
        datetime timestamp
    }
```

---

## 3. Entity Cardinality Summary

1. **User Relationships**: `users` act as creators (`1:N`) for `sources`, `notifications`, `hsn_codes`, `products`, `sales`, and `invoices`.
2. **Tax Rate Provenance**: Each `hsn_code` has zero or more `gst_rates` (`1:N`), which are anchored to a statutory CBIC `notification` (`N:1`).
3. **Rule Versioning**: Each `gst_rule` tracks historical changes in `gst_rule_versions` (`1:N`).
4. **Verification & Evidence**: Each `verification_request` yields exactly one `verification_result` (`1:1`), which cites multiple `retrieval_chunks` (`1:N`) originating from `sources`.
5. **Sales & Billing**: Each `sale` maps to one `invoice` (`1:1`), and both contain itemized child arrays (`sale_items` and `invoice_items`).
