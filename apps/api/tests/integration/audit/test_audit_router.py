"""
Integration tests for Audit Log API endpoints (/api/v1/audit/*).
"""

from smart_gst.audit.models import AuditLog


def test_audit_logs_list_and_export(client, db_session, auth_headers):
    log = AuditLog(
        id="log_test_01",
        action="INVOICE_CREATE",
        resource="INV-001",
        role="AUDITOR",
        user_id="auditor@smartgst.in",
    )
    db_session.add(log)
    db_session.commit()

    # List logs
    response = client.get("/api/v1/audit/logs", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["action"] == "INVOICE_CREATE"

    # Export JSON
    json_res = client.get("/api/v1/audit/logs/export?format=json", headers=auth_headers)
    assert json_res.status_code == 200
    assert "INVOICE_CREATE" in json_res.text

    # Export CSV
    csv_res = client.get("/api/v1/audit/logs/export?format=csv", headers=auth_headers)
    assert csv_res.status_code == 200
    assert "INVOICE_CREATE" in csv_res.text
