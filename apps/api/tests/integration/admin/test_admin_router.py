"""
Integration tests for Admin Governance & Metrics API endpoints (/api/v1/admin/*).
"""


def test_admin_metrics_authorized(client, auth_headers):
    response = client.get("/api/v1/admin/metrics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert "total_audit_events" in data
    assert "system_health" in data


def test_admin_cache_clear(client, auth_headers):
    response = client.post("/api/v1/admin/cache/clear", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "cleared" in data["message"].lower()
