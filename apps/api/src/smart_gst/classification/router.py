"""
Product Classification API Router under /api/v1/classify.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from smart_gst.classification.schemas import ClassificationRequest, ClassificationResult
from smart_gst.classification.service import ClassificationService
from smart_gst.db.session import get_db
from smart_gst.rates.repository import RateRepository

router = APIRouter(prefix="/api/v1/classify", tags=["HSN Classification"])


@router.post("", response_model=ClassificationResult)
def classify_product(payload: ClassificationRequest, db: Session = Depends(get_db)):
    rate_repo = RateRepository(db)
    service = ClassificationService(rate_repo=rate_repo)
    return service.classify_product(payload)
