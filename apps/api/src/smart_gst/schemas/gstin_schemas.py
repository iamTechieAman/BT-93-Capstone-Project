"""
GSTIN Validator Schemas.
Defines domain requests, responses, taxpayer models, and provider structures.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GSTINVerificationRequest(BaseModel):
    gstin: str = Field(..., description="15-character GSTIN to verify", example="29ABCDE1234F1ZX")
    requested_at: Optional[datetime] = None


class TaxpayerDetails(BaseModel):
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    registration_date: Optional[str] = None
    cancellation_date: Optional[str] = None
    constitution_of_business: Optional[str] = None
    taxpayer_type: Optional[str] = None
    principal_place_of_business: Optional[str] = None
    nature_of_business: Optional[List[str]] = None
    state_jurisdiction: Optional[str] = None
    center_jurisdiction: Optional[str] = None


class SourceInfo(BaseModel):
    name: str
    url: Optional[str] = None
    verified_at: datetime
    cache_hit: bool = False


class GSTINVerificationResult(BaseModel):
    gstin: str
    masked_gstin: str
    format_valid: bool
    structural_valid: bool
    checksum_valid: bool
    registration_verified: bool
    taxpayer_status: (
        str  # ACTIVE | CANCELLED | SUSPENDED | NOT_FOUND | SOURCE_UNAVAILABLE | UNKNOWN
    )
    taxpayer: Optional[TaxpayerDetails] = None
    source: SourceInfo
    verification_status: (
        str  # PENDING | RUNNING | PASSED | FAILED | SOURCE_UNAVAILABLE | REQUIRES_REVIEW
    )
    warnings: List[str] = []
    error_code: Optional[str] = None
    latency_ms: float = 0.0
