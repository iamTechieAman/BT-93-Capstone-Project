"""
Integration tests for Product Classification API endpoint (/api/v1/classify).
"""

from factories.rule_factory import TariffRuleFactory


def test_classify_endpoint_success(client, db_session):
    TariffRuleFactory.create(
        db_session, hsn_code="42031010", description="Articles of apparel, leather", rate=18.0
    )

    response = client.post(
        "/api/v1/classify",
        json={
            "product_description": "Men's genuine leather jacket with brass zip",
            "invoice_date": "2026-10-09",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["suggested_hsn"] == "42031010"
    assert data["gst_rate"] == 18.0
    assert data["status"] == "Matched"
    assert "signals" in data
    assert data["signals"]["computed_raw_confidence"] >= 75.0


def test_classify_endpoint_validation_error(client):
    response = client.post("/api/v1/classify", json={"product_description": ""})
    assert response.status_code == 422
    err = response.json()
    assert "code" in err
    assert "request_id" in err
