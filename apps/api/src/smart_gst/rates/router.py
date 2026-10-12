"""
Rate Rules & Schedule API Router under /api/v1/rules.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from smart_gst.common.errors import NotFoundException
from smart_gst.db.session import get_db
from smart_gst.rates.repository import HierarchyRepository, RateRepository
from smart_gst.rates.schemas import HierarchyNodeResponse, RateRuleResponse
from smart_gst.rates.service import RateService

router = APIRouter(tags=["Rate Rules & Schedules"])


@router.get("/api/v1/rules", response_model=List[RateRuleResponse])
@router.get("/api/v1/rates", response_model=List[RateRuleResponse])
@router.get("/api/v1/rates/search", response_model=List[RateRuleResponse])
def get_rate_rules(
    q: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    service = RateService(RateRepository(db))
    return service.list_rules(q=q, limit=limit, offset=offset)


@router.get("/api/v1/rules/search", response_model=List[RateRuleResponse])
def search_rate_rules(
    q: str = Query(default=""),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    service = RateService(RateRepository(db))
    return service.list_rules(q=q, limit=limit, offset=offset)


@router.get("/api/v1/rules/hsn/{hsn_code}", response_model=RateRuleResponse)
@router.get("/api/v1/rates/hsn/{hsn_code}", response_model=RateRuleResponse)
def get_rule_by_hsn(
    hsn_code: str = Path(..., min_length=2, max_length=10), db: Session = Depends(get_db)
):
    service = RateService(RateRepository(db))
    rule = service.get_rule_by_hsn(hsn_code)
    if not rule:
        raise NotFoundException(f"No rate rule found for HSN code '{hsn_code}'.")
    return rule


@router.get("/api/v1/rules/hierarchy/{code}", response_model=List[HierarchyNodeResponse])
@router.get("/api/v1/rates/hierarchy/{code}", response_model=List[HierarchyNodeResponse])
def get_hierarchy_chain(
    code: str = Path(..., min_length=2, max_length=10), db: Session = Depends(get_db)
):
    service = RateService(RateRepository(db), HierarchyRepository(db))
    return service.get_hierarchy(code)
