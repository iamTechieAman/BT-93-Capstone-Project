# Audit Logging Architecture & Specification

## 1. Overview & Data Governance Policy

The **Smart GST System** implements an immutable, database-level Audit Trail to guarantee compliance, traceability, and tamper-resistance across all authoritative GST datasets.

> **Data Governance Policy**: *Every data modification, whether creating/updating canonical HSN codes, adding statutory GST tax rules, registering source notifications, or re-synchronizing the Neo4j Knowledge Graph, MUST create an immutable audit record.*

---

## 2. AuditLog Schema Specification

All administrative actions are persisted in the PostgreSQL `audit_logs` table via SQLAlchemy ([`backend/app/models/database_models.py`](backend/app/models/database_models.py)).

| Field Name | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(36)` | Primary Key | Unique UUID v4 identifying the audit log entry |
| `user_id` | `VARCHAR(100)` | Not Null | User ID / Subject responsible for the administrative action |
| `action` | `VARCHAR(100)` | Not Null | Standardized action code (e.g. `CREATE_HSN`, `UPDATE_HSN`, `CREATE_GST_RULE`, `CREATE_SOURCE`, `SYNC_KNOWLEDGE_GRAPH`) |
| `target_entity` | `VARCHAR(100)` | Not Null | Target table or system component (e.g. `hsn_codes`, `gst_rules`, `sources`, `neo4j_graph`) |
| `target_id` | `VARCHAR(100)` | Not Null | Unique identifier of the created/modified record or system target |
| `timestamp` | `TIMESTAMP (UTC)` | Not Null, Default `utcnow` | Microsecond-precision UTC timestamp of execution |

---

## 3. Audited Administrative Operations

| Endpoint | Action Code | Target Entity | Audit Triggered |
| :--- | :--- | :--- | :---: |
| `POST /api/v1/admin/hsn` | `CREATE_HSN` / `UPDATE_HSN` | `hsn_codes` |  Mandatory |
| `POST /api/v1/admin/gst-rules` | `CREATE_GST_RULE` | `gst_rules` |  Mandatory |
| `POST /api/v1/admin/sources` | `CREATE_SOURCE` | `sources` |  Mandatory |
| `POST /api/v1/admin/sync-graph` | `SYNC_KNOWLEDGE_GRAPH` | `neo4j_graph` |  Mandatory |

---

## 4. Audit Repository Architecture

The `AuditRepository` class ([`backend/app/repositories/app_repositories.py`](backend/app/repositories/app_repositories.py)) provides atomic transactional logging:

```python
class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log_action(self, action: str, target_entity: str, target_id: str, user_id: str) -> AuditLog:
        audit_entry = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            target_entity=target_entity,
            target_id=target_id,
            timestamp=datetime.utcnow()
        )
        self.db.add(audit_entry)
        self.db.commit()
        self.db.refresh(audit_entry)
        return audit_entry
```

---

## 5. Audit Log Inspection & Security Access

Audit logs can be queried via `GET /api/v1/admin/audit-logs`. Access is strictly restricted to authenticated users with `ADMIN` or `COMPLIANCE_OFFICER` roles via the `require_admin` dependency. Requests from unauthenticated or regular `USER` accounts are blocked with `403 Forbidden`.
