# Role-Based Access Control (RBAC) Specification

## 1. Overview & Security Guardrail

The **Smart GST System** enforces Role-Based Access Control (RBAC) across all API routes and data management interfaces.

> **Mandatory Security Rule**: *No regular user should be allowed to modify authoritative GST knowledge.*

Only authenticated users with the `ADMIN` or `COMPLIANCE_OFFICER` role are permitted to create, update, or deactivate canonical HSN codes, statutory GST rules, or source notifications. Regular users (`USER` role) attempting administrative modifications receive an immediate `403 Forbidden` response.

---

## 2. Roles & Permissions Matrix

| Role | Read HSN / GST Data | Execute Verification | Submit Sales & Invoices | Modify Authoritative HSN / GST Rules | View Audit Logs | Trigger Graph Sync |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `USER` |  |  |  |  (403 Forbidden) |  (403 Forbidden) |  (403 Forbidden) |
| `COMPLIANCE_OFFICER` |  |  |  |  |  |  |
| `ADMIN` |  |  |  |  |  |  |

---

## 3. JWT Authentication & Dependency Enforcement

Endpoints enforcing admin authorization consume the `require_admin` dependency ([`backend/app/core/security.py`](backend/app/core/security.py)):

```python
def require_admin(user_payload: dict = Depends(get_current_user_payload)) -> dict:
    role = user_payload.get("role", "USER").upper()
    if role not in ["ADMIN", "COMPLIANCE_OFFICER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Admin or Compliance Officer privileges required to modify authoritative GST knowledge."
        )
    return user_payload
```
