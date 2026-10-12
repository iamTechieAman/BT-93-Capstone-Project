"""
Classification Request, Response, and Real-Signal Breakdown Schemas.
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ClassificationRequest(BaseModel):
    product_description: str = Field(
        ..., min_length=2, description="Product description or query text"
    )
    mode: Literal["INTRA_STATE", "INTER_STATE"] = "INTRA_STATE"
    invoice_date: str = Field(default="2026-10-09")
    attributes: Optional[Dict[str, Any]] = None


class SignalBreakdown(BaseModel):
    keyword_match_score: float = Field(..., description="TF-IDF keyword score 0-100")
    vector_similarity_score: float = Field(
        ..., description="Vector embedding cosine similarity 0-100"
    )
    statutory_rule_match: bool = Field(
        ..., description="Whether exact schedule rule was identified"
    )
    agreeing_sources_count: int = Field(..., description="Count of distinct CBIC sources agreeing")
    missing_conditions_penalty: float = Field(
        ..., description="Penalty for unanswered conditional criteria"
    )
    computed_raw_confidence: float = Field(..., description="Computed raw confidence score (0-100)")


class SourceEvidence(BaseModel):
    document: str
    notification: str
    notification_date: str
    schedule: str
    serial_no: str
    effective_from: str
    retrieved_at: str
    url: str


class CandidateAlternative(BaseModel):
    hsn_code: str
    description: str
    score: float


class ClassificationResult(BaseModel):
    product_description: str
    suggested_hsn: str
    hsn_description: str
    chapter: str
    heading: str
    gst_rate: float
    effective_rate_text: str
    match_quality: Literal["Strong", "Moderate", "Weak"]
    status: Literal["Matched", "Needs review"]
    confidence: float
    signals: SignalBreakdown
    sources: List[SourceEvidence] = []
    alternatives_considered: List[CandidateAlternative] = []
    reasoning_summary: str
    evaluation_factors: List[str] = []
