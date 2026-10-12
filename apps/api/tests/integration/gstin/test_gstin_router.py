"""
Integration tests for GSTIN Verification API endpoint (/api/v1/gstin/*).
"""


def test_gstin_verify_endpoint_valid(client):
    response = client.get("/api/v1/gstin/27AAPFU0939F1ZV")
    assert response.status_code == 200
    data = response.json()
    assert data["format_valid"] is True
    assert data["verification_status"] == "PASSED"
    assert data["state_name"] == "Maharashtra"
    assert data["headline"] == "Format valid. Registration not verified."


def test_gstin_verify_endpoint_invalid_checksum(client):
    response = client.get("/api/v1/gstin/27AAPFU0939F1ZX")
    assert response.status_code == 200
    data = response.json()
    assert data["format_valid"] is False
    assert data["checksum_valid"] is False
    assert data["verification_status"] == "FAILED"
