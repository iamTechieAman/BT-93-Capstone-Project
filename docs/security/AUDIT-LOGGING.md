# Statutory GST Audit Logging & Compliance Specification

## 1. Executive Overview
The **Smart GST Verifier & Compliance Engine** maintains an append-only, immutable audit trail for every AI product classification, tax rate determination, invoice finalization, and data administration action. This specification documents the architecture, security guarantees, 16-point audit record schema, search/filtering API, and immutability controls enforced in accordance with statutory tax governance guidelines.

---

## 2. Immutability & Security Controls
1. **Append-Only Enforcement**: Audit records (`audit_logs` table) are created via atomic database inserts. Modifying or deleting existing audit logs is strictly prohibited (`DELETE` and `PUT` endpoints return `HTTP 403 Forbidden`).
2. **Role-Based Access Control (RBAC)**: Access to statutory audit logs is restricted to authenticated users with `ADMIN`, `AUDITOR`, or `COMPLIANCE_OFFICER` roles.
3. **Cryptographic Timestamps**: Timestamps are generated using UTC system clocks (`datetime.now(timezone.utc)`). Timestamps cannot be overridden or faked by client requests.

---

## 3. The 16 Statutory Audit Dimensions

Every AI classification decision audit entry captures 16 explicit dimensions:

| # | Audit Field | Description | Type / Format |
|---|---|---|---|
| **1** | `timestamp` | UTC ISO-8601 execution timestamp | String (ISO-8601) |
| **2** | `user` | Authenticated user ID or system service actor | String (UUID / Email) |
| **3** | `input` | Raw user product description query | String |
| **4** | `normalized_input` | Pre-processed tokens, lemmatized form, and extracted entities | JSON Object |
| **5** | `candidate_codes` | Top retrieved candidate HSN/SAC codes with vector scores | JSON Array |
| **6** | `retrieved_evidence` | Retrieved CBIC notification chunks, excerpts, and URLs | JSON Array |
| **7** | `graph_relationships` | Neo4j Knowledge Graph ontology facts and traversed edges | JSON Array |
| **8** | `selected_rule` | Statutory GST tax schedule rule matched | JSON Object |
| **9** | `llm_provider / model` | LLM abstraction provider & model ID (e.g. Gemini 1.5 Pro) | String |
| **10** | `structured_model_output` | Raw structured JSON response returned by LLM abstraction | JSON Object |
| **11** | `deterministic_validation` | Outcomes of 10-point statutory domain engine checks | JSON Object |
| **12** | `final_result` | Selected code, code_type, GST rate, and tax calculation | JSON Object |
| **13** | `confidence` | Derived overall, classification, tax, and evidence confidence | JSON Object |
| **14** | `warnings` | Ambiguity markers or rule execution warnings | JSON Array |
| **15** | `human_review_status` | Flag indicating if manual human review is required | Boolean |
| **16** | `source_version` | Authoritative CBIC notification tariff schedule version | String |

---

## 4. API Search, Filtering, and Export Features

### Query Parameters (`GET /api/v1/audit` or `GET /api/v1/admin/audit-logs`)
- `query`: Keyword text search on action, entity, user, or product.
- `action`: Filter by specific audit action (e.g., `VERIFY_PRODUCT`, `CREATE_HSN`, `CREATE_INVOICE`).
- `start_date` / `end_date`: ISO date range filtering (`YYYY-MM-DD`).
- `skip` / `limit`: Pagination controls.

### Export Formats
- `GET /api/v1/audit/export/json`: Downloads full audit records formatted in standardized JSON.
- `GET /api/v1/audit/export/csv`: Exports audit records formatted in tabular CSV for tax auditors.
