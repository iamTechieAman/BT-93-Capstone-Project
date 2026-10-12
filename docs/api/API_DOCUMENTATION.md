# FastAPI Backend API Specification & Documentation

## Executive Overview

The **Smart GST Verification & Manufacturing Sales Automation System** backend is built on **FastAPI** using a modular, layered architecture:
```text
HTTP Routes (api/v1/*.py)  Service Layer (services/*.py)  Domain Logic & Repositories (repositories/*.py)  Providers / Database
```

All 11 required endpoints are mounted under the versioned base path `/api/v1`. Interactive OpenAPI documentation is accessible at `/api/v1/docs` (Swagger UI) and `/api/v1/redoc` (ReDoc).

---

##  API Endpoint Directory (`/api/v1`)

| Endpoint Prefix | Method(s) | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/api/v1/auth` | `POST /register`, `POST /login`, `GET /me` | User registration, authentication, token issuance, and current user profile | Public / Bearer |
| `/api/v1/products` | `GET /`, `POST /`, `GET /{id}` | Product catalog management and search | Public / Bearer |
| `/api/v1/hsn` | `GET /`, `GET /search`, `GET /{hsn_code}` | HSN code search, tariff hierarchy, and description lookups | Public |
| `/api/v1/gst` | `GET /rates/{hsn_code}`, `GET /rules/{hsn_code}` | Statutory GST rate schedule and conditional rule lookups | Public |
| `/api/v1/verify` | `POST /` | 8-Stage Smart GST Verification Engine execution | Public / Bearer |
| `/api/v1/rag` | `POST /search` | RAG hybrid document search across CBIC notifications and circulars | Public |
| `/api/v1/knowledge-graph` | `POST /query`, `POST /validate` | Neo4j Cypher ontology queries and triple validation | Public |
| `/api/v1/sales` | `GET /`, `POST /`, `GET /{id}` | ERP Sales order management and line item creation | Bearer |
| `/api/v1/invoices` | `GET /`, `POST /`, `POST /validate` | GST Tax Invoice generation and mathematical tax split validation | Bearer |
| `/api/v1/reports` | `GET /compliance-summary` | Overall compliance stats, sales summary, and tax breakdown | Bearer / Admin |
| `/api/v1/admin` | `GET /audit-logs`, `POST /reindex-dataset`, `GET /system-status` | System audit logs, vector search re-indexing, and service status | Admin |

---

##  Key Endpoint Details & Schemas

### 1. Verification Engine (`POST /api/v1/verify`)
- **Request Body**:
  ```json
  {
    "product_description": "Genuine bovine leather biker jacket with asymmetrical front zip",
    "is_inter_state": false
  }
  ```
- **Response Structure (200 OK)**:
  ```json
  {
    "product_input": "Genuine bovine leather biker jacket with asymmetrical front zip",
    "suggested_hsn": "42031010",
    "chapter": "42",
    "chapter_name": "Articles of Leather",
    "description": "Articles of apparel and clothing accessories, of leather or of composition leather - Jackets and blazers",
    "gst_rate": 18.0,
    "cgst": 9.0,
    "sgst": 9.0,
    "igst": 18.0,
    "cess": 0.0,
    "unit": "Pcs",
    "confidence": 96.0,
    "reasoning_why": "The retrieved GST rule identifies heading 4203 for articles of apparel of leather.",
    "evidence": [
      {
        "label": "HSN Record Match",
        "verified": true,
        "detail": "HSN 42031010 matched in official schedule.",
        "effective_date": "2017-07-01",
        "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf"
      }
    ],
    "stages": [
      { "stage_id": 1, "name": "Text Pre-processing", "status": "completed" },
      { "stage_id": 2, "name": "Candidate Retrieval", "status": "completed" },
      { "stage_id": 3, "name": "RAG Retrieval", "status": "completed" },
      { "stage_id": 4, "name": "Knowledge Graph Validation", "status": "completed" },
      { "stage_id": 5, "name": "LLM Reasoning Engine", "status": "completed" },
      { "stage_id": 6, "name": "GST Rate Computation", "status": "completed" },
      { "stage_id": 7, "name": "Confidence & Evidence Validation", "status": "completed" }
    ]
  }
  ```

---

### 2. Invoice Creation (`POST /api/v1/invoices`)
- **Request Body**:
  ```json
  {
    "sale_id": "g1111111-1111-1111-1111-111111111111",
    "invoice_number": "INV-2026-001",
    "place_of_supply": "27-Maharashtra",
    "supplier_gstin": "27AAACG98761Z2",
    "customer_gstin": "27AAACA12341Z5"
  }
  ```
- **Response Structure (200 OK)**:
  ```json
  {
    "id": "i1111111-1111-1111-1111-111111111111",
    "sale_id": "g1111111-1111-1111-1111-111111111111",
    "invoice_number": "INV-2026-001",
    "total_taxable_value": 17000.0,
    "total_cgst": 1530.0,
    "total_sgst": 1530.0,
    "total_igst": 0.0,
    "grand_total": 20060.0,
    "is_validated": true,
    "validation_notes": "GST calculation verified deterministically against statutory rate schedule."
  }
  ```

---

##  Centralized Error & Exception Format

Uncaught exceptions, Pydantic schema validation failures, and HTTP errors follow a unified JSON envelope:

```json
{
  "error": true,
  "code": 422,
  "message": "Request validation failed",
  "details": [
    {
      "loc": ["body", "product_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "path": "/api/v1/products"
}
```
