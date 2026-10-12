"""
GSTIN Verification API Router under /api/v1/gstin.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from smart_gst.db.session import get_db
from smart_gst.gstin.repository import GstinCacheRepository
from smart_gst.gstin.schemas import GstinVerifyResponse
from smart_gst.gstin.service import GstinService, normalize_gstin

router = APIRouter(prefix="/api/v1/gstin", tags=["GSTIN Verification"])


class GstinVerifyRequest(BaseModel):
    gstin: str = Field(..., min_length=1)


@router.post("/verify", response_model=GstinVerifyResponse)
def verify_gstin_post(payload: GstinVerifyRequest, db: Session = Depends(get_db)):
    cleaned = normalize_gstin(payload.gstin)
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="GSTIN parameter cannot be empty."
        )

    cache_repo = GstinCacheRepository(db)
    service = GstinService(cache_repo)
    return service.verify_gstin(cleaned)


@router.get("/{gstin}", response_model=GstinVerifyResponse)
def verify_gstin(gstin: str, db: Session = Depends(get_db)):
    cleaned = normalize_gstin(gstin)
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="GSTIN parameter cannot be empty."
        )

    cache_repo = GstinCacheRepository(db)
    service = GstinService(cache_repo)
    return service.verify_gstin(cleaned)
