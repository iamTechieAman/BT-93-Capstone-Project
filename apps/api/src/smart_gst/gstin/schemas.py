"""
GSTIN Pydantic Verification Schemas.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel


class StepStatus(BaseModel):
    id: str
    name: str
    state: Literal["PASSED", "FAILED", "SKIPPED"]
    detail: Optional[str] = None


class GstinVerifyResponse(BaseModel):
    gstin: str
    masked_gstin: str
    format_valid: bool
    structural_valid: bool
    checksum_valid: bool
    registration_verified: bool
    taxpayer_status: str
    headline: str
    verification_status: Literal[
        "PASSED", "FAILED", "SKIPPED", "REQUIRES_REVIEW", "VALID", "INVALID"
    ]
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    pan: Optional[str] = None
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    registration_date: Optional[str] = None
    constitution: Optional[str] = None
    jurisdiction: Optional[str] = None
    address: Optional[str] = None
    provider_name: Optional[str] = None
    fetched_at: Optional[str] = None
    cached: bool = False
    validation_failures: List[str] = []
    steps: List[StepStatus] = []
    warnings: List[str] = []
    error_code: Optional[str] = None
    latency_ms: float = 0.0
