"""
Rate Rules & Relational Hierarchy Repository.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from smart_gst.rates.models import TariffHierarchy, TariffRateRule


class RateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_hsn(self, hsn_code: str) -> Optional[TariffRateRule]:
        return (
            self.db.query(TariffRateRule)
            .filter(TariffRateRule.hsn_code.like(f"{hsn_code}%"))
            .first()
        )

    def list_all(self, limit: int = 50, offset: int = 0) -> List[TariffRateRule]:
        return self.db.query(TariffRateRule).offset(offset).limit(limit).all()

    def search(self, q: str, limit: int = 50, offset: int = 0) -> List[TariffRateRule]:
        pattern = f"%{q}%"
        return (
            self.db.query(TariffRateRule)
            .filter(
                (TariffRateRule.hsn_code.ilike(pattern))
                | (TariffRateRule.description.ilike(pattern))
            )
            .offset(offset)
            .limit(limit)
            .all()
        )


class HierarchyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, code: str) -> Optional[TariffHierarchy]:
        return self.db.query(TariffHierarchy).filter(TariffHierarchy.code == code).first()

    def get_ancestor_chain(self, code: str) -> List[TariffHierarchy]:
        """Fetch chain from Chapter down to Tariff Item."""
        chain = []
        current = self.get_by_code(code)
        while current:
            chain.insert(0, current)
            if not current.parent_id:
                break
            current = self.get_by_code(current.parent_id)
        return chain
