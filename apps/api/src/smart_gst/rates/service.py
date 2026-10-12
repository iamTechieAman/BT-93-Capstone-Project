"""
Rate & Statutory Schedule Service.
"""

from typing import List, Optional

from smart_gst.rates.repository import HierarchyRepository, RateRepository
from smart_gst.rates.schemas import HierarchyNodeResponse, RateRuleResponse


class RateService:
    def __init__(
        self, rate_repo: RateRepository, hierarchy_repo: Optional[HierarchyRepository] = None
    ):
        self.rate_repo = rate_repo
        self.hierarchy_repo = hierarchy_repo

    def get_rule_by_hsn(self, hsn_code: str) -> Optional[RateRuleResponse]:
        rule = self.rate_repo.get_by_hsn(hsn_code)
        return RateRuleResponse.model_validate(rule) if rule else None

    def list_rules(
        self, q: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[RateRuleResponse]:
        if q:
            rules = self.rate_repo.search(q=q, limit=limit, offset=offset)
        else:
            rules = self.rate_repo.list_all(limit=limit, offset=offset)
        return [RateRuleResponse.model_validate(r) for r in rules]

    def get_hierarchy(self, code: str) -> List[HierarchyNodeResponse]:
        if not self.hierarchy_repo:
            return []
        chain = self.hierarchy_repo.get_ancestor_chain(code)
        return [HierarchyNodeResponse.model_validate(node) for node in chain]
