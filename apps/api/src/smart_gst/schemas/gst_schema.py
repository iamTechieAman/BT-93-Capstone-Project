from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EntityExtraction(BaseModel):
    materials: List[str] = []
    item_types: List[str] = []
    accessories: List[str] = []
    qualifiers: List[str] = []


class HsnCandidate(BaseModel):
    hsn_code: str
    chapter: str
    description: str
    score: float


class KgTriple(BaseModel):
    subject: str
    predicate: str
    object: str


class EvidenceItem(BaseModel):
    label: str
    verified: bool
    detail: str
    source: Optional[str] = "CBIC"
    document: Optional[str] = "Statutory GST Rate Schedule"
    notification: Optional[str] = "Notification No. 1/2017-Central Tax (Rate)"
    date: Optional[str] = "2017-06-28"
    effective_date: Optional[str] = "2017-07-01"
    effective_period: Optional[str] = "2017-07-01 to Present"
    excerpt: Optional[str] = None
    source_url: Optional[str] = "https://cbic-gst.gov.in"
    url: Optional[str] = "https://cbic-gst.gov.in"
    retrieved_at: Optional[str] = None


class PipelineStage(BaseModel):
    stage_id: int
    name: str
    status: str = "COMPLETED"  # PENDING, RUNNING, COMPLETED, FAILED, SKIPPED, REVIEW_REQUIRED
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_ms: Optional[float] = 0.0
    duration: Optional[str] = "0.0ms"
    relevant_output: Dict[str, Any] = {}
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class VerificationRequest(BaseModel):
    product_description: str = Field(..., json_schema_extra={"example": "Leather Jacket with Zip"})
    is_inter_state: bool = False


class VerificationResponse(BaseModel):
    product_input: str
    suggested_hsn: str
    chapter: str
    chapter_name: str
    description: str
    gst_rate: float
    cgst: float
    sgst: float
    igst: float
    cess: float = 0.0
    unit: str = "Pcs"
    classification_confidence: float
    tax_confidence: float
    evidence_confidence: float
    overall_confidence: float
    confidence: float
    tax_rate_confidence: float
    result_state: str = "VERIFIED"
    reasoning_why: str
    evidence: List[EvidenceItem]
    extracted_entities: EntityExtraction
    top_candidates: List[HsnCandidate]
    kg_triples: List[KgTriple]
    stages: List[PipelineStage]
