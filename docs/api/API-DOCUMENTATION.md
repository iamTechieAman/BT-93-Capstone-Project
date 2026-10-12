# Smart GST System — Production API Documentation v1.0

## 1. Overview & Architecture Design

The Smart GST System API is built with **FastAPI** following a strict 5-tier layered architecture:
```
API Route Router  Service Layer  Domain Engine  Repository Layer  Database / Vector Provider
```

### Key Architectural Safeguards
- **Zero Business Logic in Routers**: API handlers only unpack HTTP requests, inject services via FastAPI dependency injection, and return Pydantic schemas.
- **LLM Abstraction**: LLM reasoning is completely isolated in `GeminiLLMProvider` ([`backend/app/llm/llm_provider.py`](backend/app/llm/llm_provider.py)), separating AI inference from business domain code.
- **Request ID Tracking**: Every HTTP response includes an `X-Request-ID` header for distributed tracing.
- **Security & RBAC**: Mandatory HMAC-SHA256 bearer token validation with role enforcement (`ADMIN`, `COMPLIANCE_OFFICER`, `AUDITOR`, `USER`).

---

## 2. Global Request & Response Specifications

### Headers
| Header Name | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | `string` | Optional / Required | Bearer token format: `Bearer <token>` |
| `X-Request-ID` | `string` | Optional | Client-assigned or server-generated UUID tracing tag |
| `Content-Type` | `string` | Required | `application/json` for POST/PUT requests |

### Standard Error Response Format
All error responses (400, 401, 403, 404, 422, 429, 500) follow a standardized JSON envelope:
```json
{
  "error": true,
  "code": 404,
  "message": "HSN Code 99999999 not found",
  "path": "/api/v1/hsn/99999999"
}
```

---

## 3. Versioned Endpoint Catalog (`/api/v1`)

### 3.1 Authentication & User Management (`/api/v1/auth`)
- `POST /api/v1/auth/register`: Register a new user account.
- `POST /api/v1/auth/login`: Authenticate user credentials and issue signed JWT access token.

### 3.2 Product Catalog API (`/api/v1/products`)
- `GET /api/v1/products`: Search and filter master product catalog.
- `POST /api/v1/products`: Create a new catalog item.
- `GET /api/v1/products/{product_id}`: Retrieve product details by ID.

### 3.3 Goods HSN Code API (`/api/v1/hsn`)
- `POST /api/v1/hsn/classify`: Match natural-language product queries against 8-digit HSN codes using hybrid vector search.
- `GET /api/v1/hsn`: Search HSN database.
- `GET /api/v1/hsn/{hsn_code}`: Fetch HSN code metadata, chapter, and classification level.

### 3.4 Services SAC Code API (`/api/v1/sac`)
- `GET /api/v1/sac`: Search SAC database for 6-digit service codes.
- `GET /api/v1/sac/search?q={query}`: Search SAC codes by pattern.
- `GET /api/v1/sac/{sac_code}`: Retrieve SAC code description and category.

### 3.5 Statutory GST Rates & Rules API (`/api/v1/gst`)
- `GET /api/v1/gst/rates/{hsn_code}`: Fetch statutory tax rates (CGST, SGST, IGST, Cess).
- `GET /api/v1/gst/rules/{hsn_code}`: Retrieve tax conditions and exemption notifications.

### 3.6 Smart GST Verification Engine (`/api/v1/verify`)
- `POST /api/v1/verify`: Trigger 8-stage verification pipeline (Preprocessing -> TF-IDF/Vector Search -> RAG -> Knowledge Graph -> Explainable LLM Reasoning -> Rate Computation -> Evidence Validation).

### 3.7 RAG Legal Knowledge Library (`/api/v1/rag`)
- `POST /api/v1/rag/search`: Hybrid retrieval across Central Tax notifications, circulars, and Advance Rulings.

### 3.8 Knowledge Graph Explorer (`/api/v1/knowledge-graph`)
- `POST /api/v1/knowledge-graph/query`: Traverses Neo4j graph ontology for material-category-tax relationships.

### 3.9 Sales Transactions API (`/api/v1/sales`)
- `POST /api/v1/sales`: Record commercial sales transaction with itemized tax values.
- `GET /api/v1/sales`: List sales history.
- `GET /api/v1/sales/{sale_id}`: Retrieve sale order details.

### 3.10 Invoices & Validation API (`/api/v1/invoices`)
- `POST /api/v1/invoices`: Generate Rule 46 compliant GST tax invoice from confirmed sale.
- `POST /api/v1/invoices/validate`: Audit line-item tax calculations deterministically.

### 3.11 Compliance Audit Trail API (`/api/v1/audit`)
- `GET /api/v1/audit`: List immutable audit logs for data modifications (`ADMIN`, `AUDITOR`, `COMPLIANCE_OFFICER` required).
- `GET /api/v1/audit/{log_id}`: Fetch detailed audit record.

### 3.12 System Governance & Admin API (`/api/v1/admin`)
- `GET /api/v1/admin/audit-logs`: Admin log viewer.
- `GET /api/v1/admin/governance-status`: Monitor system health, RAG state, and KG connectivity.

---

## 4. OpenAPI & Swagger UI
The interactive Swagger API documentation and OpenAPI schema are hosted at:
- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc UI**: `http://localhost:8000/api/v1/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/v1/openapi.json`
