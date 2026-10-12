"""
Unit tests for Relational Tariff Hierarchy taxonomy structure.
"""

from smart_gst.rates.models import TariffHierarchy
from smart_gst.rates.repository import HierarchyRepository


def test_tariff_hierarchy_ancestor_chain(db_session):
    # Insert chapter -> heading -> sub-heading -> tariff item
    ch = TariffHierarchy(code="42", level="chapter", title="Articles of leather", parent_id=None)
    hd = TariffHierarchy(code="4203", level="heading", title="Articles of apparel", parent_id="42")
    sub = TariffHierarchy(
        code="420310", level="sub_heading", title="Articles of apparel", parent_id="4203"
    )
    item = TariffHierarchy(
        code="42031010", level="tariff_item", title="Jackets and trousers", parent_id="420310"
    )

    db_session.add_all([ch, hd, sub, item])
    db_session.commit()

    repo = HierarchyRepository(db_session)
    chain = repo.get_ancestor_chain("42031010")

    assert len(chain) == 4
    assert chain[0].code == "42"
    assert chain[1].code == "4203"
    assert chain[2].code == "420310"
    assert chain[3].code == "42031010"


def test_rate_service_methods(db_session):
    from factories.rule_factory import TariffRuleFactory

    from smart_gst.rates.repository import HierarchyRepository, RateRepository
    from smart_gst.rates.service import RateService

    TariffRuleFactory.create(
        db_session, hsn_code="42031010", description="Leather Jackets", rate=18.0
    )

    rate_repo = RateRepository(db_session)
    hierarchy_repo = HierarchyRepository(db_session)
    service = RateService(rate_repo, hierarchy_repo)

    # get_rule_by_hsn
    res = service.get_rule_by_hsn("4203")
    assert res is not None
    assert res.rate == 18.0

    # None case
    assert service.get_rule_by_hsn("99999") is None

    # list_rules with and without query
    assert len(service.list_rules()) >= 1
    assert len(service.list_rules(q="Leather")) >= 1
    assert len(service.list_rules(q="NonExistentProduct")) == 0

    # hierarchy without repo
    service_no_hier = RateService(rate_repo)
    assert service_no_hier.get_hierarchy("4203") == []
