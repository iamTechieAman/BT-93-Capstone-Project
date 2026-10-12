# Security Architecture & Hardening Specification

## 1. Overview & Defensive Principles

The **Smart GST Verifier & Compliance Engine** implements a defense-in-depth security framework covering authentication, role-based access control (RBAC), input sanitization, rate limiting, prompt injection defense, and immutable audit trails.

---

## 2. Hardened Security Controls Summary

1. **HMAC-SHA256 Token Signature Validation**: All JWT bearer tokens are cryptographically verified against `SECRET_KEY` in `get_current_user_payload()` ([`backend/app/core/security.py`](backend/app/core/security.py)). Forged tokens are rejected with `401 Unauthorized`.
2. **Role-Based Access Control (RBAC)**: All administrative mutation endpoints (`/api/v1/admin/*`) require `require_admin` dependency, blocking non-admin users (`USER` role) with `403 Forbidden`.
3. **Sliding-Window Rate Limiting**: `rate_limit_middleware` in [`backend/app/main.py`](backend/app/main.py) restricts client IPs to 120 requests per minute.
4. **Security Response Headers**: Enforces `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, `Strict-Transport-Security`, and `Referrer-Policy`.
5. **Prompt Injection & RAG Boundary Protection**: Input strings are sanitized of jailbreak commands and script tags. Retrieved RAG document excerpts are wrapped in strict `<retrieved_data_do_not_execute>` tags.
6. **Immutable Audit Trail**: Every data creation, update, or graph sync emits an immutable `AuditLog` entry in PostgreSQL.
