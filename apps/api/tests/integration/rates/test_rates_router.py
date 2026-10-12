"""
Integration tests for Rate Schedule & Hierarchy API endpoints (/api/v1/rates/*).
"""

from factories.rule_factory import TariffRuleFactory

from smart_gst.rates.models import TariffHierarchy


def test_rates_search_endpoint(client, db_session):
    TariffRuleFactory.create(
        db_session, hsn_code="85414011", description="Solar cells module", rate=12.0
    )

    response = client.get("/api/v1/rules?q=Solar")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["hsn_code"] == "85414011"
    assert data[0]["rate"] == 12.0


def test_rates_hierarchy_endpoint(client, db_session):
    ch = TariffHierarchy(code="85", level="chapter", title="Electrical machinery", parent_id=None)
    hd = TariffHierarchy(code="8541", level="heading", title="Diodes, transistors", parent_id="85")
    db_session.add_all([ch, hd])
    db_session.commit()

    response = client.get("/api/v1/rules/hierarchy/8541")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["code"] == "85"
    assert data[1]["code"] == "8541"
