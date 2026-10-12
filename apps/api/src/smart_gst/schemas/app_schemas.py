"""
Pydantic v2 Input/Output Schemas for Smart GST System.
Enforces request validation, strict type safety, and clean API responses.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- AUTH SCHEMAS ---
class UserLoginRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@acme-corp.com"})
    password: str = Field(..., json_schema_extra={"example": "secret123"})


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "newuser@company.com"})
    full_name: str = Field(..., min_length=2, json_schema_extra={"example": "Aman Kumar"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "secret123"})
    role: Optional[str] = Field("USER", json_schema_extra={"example": "USER"})


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# --- PRODUCT SCHEMAS ---
class ProductCreateRequest(BaseModel):
    product_name: str = Field(
        ..., min_length=2, json_schema_extra={"example": "Leather Biker Jacket"}
    )
    product_description: str = Field(
        ...,
        min_length=5,
        json_schema_extra={"example": "Genuine bovine leather jacket with side zip"},
    )
    material: Optional[str] = Field("Leather", json_schema_extra={"example": "Leather"})
    category: Optional[str] = Field("Apparel", json_schema_extra={"example": "Apparel"})
    hsn_code_id: Optional[str] = None
    unit_price: float = Field(0.0, ge=0.0, json_schema_extra={"example": 8500.0})


class ProductResponse(BaseModel):
    id: str
    product_name: str
    product_description: str
    material: Optional[str]
    category: Optional[str]
    hsn_code_id: Optional[str]
    unit_price: float
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- HSN SCHEMAS ---
class HsnCodeResponse(BaseModel):
    id: str
    hsn_code: str
    hsn_level: str
    chapter: str
    heading: Optional[str]
    subheading: Optional[str]
    technical_description: str
    trade_description: Optional[str]
    category: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class SacCodeResponse(BaseModel):
    id: str
    sac_code: str
    chapter: str
    heading: Optional[str]
    description: str
    category: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class HsnClassificationRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        json_schema_extra={
            "example": "Men's biker style genuine leather jacket with metallic zipper"
        },
    )
    top_k: int = Field(5, ge=1, le=20)
    category_filter: Optional[str] = Field(
        None, json_schema_extra={"example": "Apparel & Accessories"}
    )
    chapter_filter: Optional[str] = Field(None, json_schema_extra={"example": "42"})
    material_filter: Optional[str] = Field(None, json_schema_extra={"example": "Leather"})
    max_gst_rate: Optional[float] = Field(None, json_schema_extra={"example": 18.0})


class HsnClassificationCandidate(BaseModel):
    hsn_code: str
    chapter: str
    heading: str
    description: str
    trade_description: Optional[str] = None
    match_score: float
    matched_attributes: List[str] = []
    evidence: str
    source: str
    gst_rate: float
    cgst_rate: float
    sgst_rate: float
    igst_rate: float
    cess_rate: float = 0.0
    conditions: Optional[str] = None
    code_type: str = "HSN"


class HsnClassificationResponse(BaseModel):
    query: str
    total_candidates_found: int
    top_candidates: List[HsnClassificationCandidate]


class ClassificationEngineRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        json_schema_extra={"example": "IT software development and cloud consulting services"},
    )
    top_k: int = Field(5, ge=1, le=20)
    category_filter: Optional[str] = None
    material_filter: Optional[str] = None


class ClassificationEngineResponse(BaseModel):
    classification_status: str
    code_type: str
    selected_code: str
    description: str
    top_candidates: List[HsnClassificationCandidate]
    matched_attributes: List[str]
    classification_confidence: float
    evidence_ids: List[str]
    warnings: List[str]
    needs_human_review: bool


# --- GST SCHEMAS ---
class GstRateResponse(BaseModel):
    id: str
    hsn_code_id: str
    gst_rate: float
    cgst_rate: float
    sgst_rate: float
    igst_rate: float
    cess_rate: float
    effective_from: date
    effective_to: Optional[date]
    model_config = ConfigDict(from_attributes=True)


class GstRuleResponse(BaseModel):
    id: str
    hsn_code_id: str
    rule_name: str
    conditions: str
    exceptions: Optional[str]
    effective_from: date
    effective_to: Optional[date]
    model_config = ConfigDict(from_attributes=True)


# --- SALES SCHEMAS ---
class SaleItemRequest(BaseModel):
    product_id: str
    hsn_code_id: str
    quantity: float = Field(1.0, gt=0)
    unit_price: float = Field(..., ge=0)
    taxable_value: float = Field(..., ge=0)
    gst_rate: float = Field(..., ge=0)


class SaleCreateRequest(BaseModel):
    sale_number: str = Field(..., json_schema_extra={"example": "SAL-2026-001"})
    customer_name: str = Field(..., json_schema_extra={"example": "Apex Manufacturing Ltd"})
    customer_gstin: Optional[str] = Field(
        "27AAACA12341Z5", json_schema_extra={"example": "27AAACA12341Z5"}
    )
    sale_date: Optional[date] = Field(default_factory=date.today)
    items: List[SaleItemRequest]


class SaleResponse(BaseModel):
    id: str
    sale_number: str
    customer_name: str
    customer_gstin: Optional[str]
    sale_date: date
    status: str
    total_amount: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- INVOICE SCHEMAS ---
class InvoiceCreateRequest(BaseModel):
    sale_id: str
    invoice_number: str = Field(..., json_schema_extra={"example": "INV-2026-001"})
    invoice_date: Optional[date] = Field(default_factory=date.today)
    place_of_supply: str = Field("27-Maharashtra", json_schema_extra={"example": "27-Maharashtra"})
    supplier_gstin: str = Field("27AAACG98761Z2", json_schema_extra={"example": "27AAACG98761Z2"})
    customer_gstin: Optional[str] = Field(
        "27AAACA12341Z5", json_schema_extra={"example": "27AAACA12341Z5"}
    )


class InvoiceValidationRequest(BaseModel):
    invoice_number: str
    supplier_gstin: str
    customer_gstin: Optional[str]
    place_of_supply: str
    line_items: List[Dict[str, Any]]


class InvoiceResponse(BaseModel):
    id: str
    sale_id: str
    invoice_number: str
    invoice_date: date
    place_of_supply: str
    supplier_gstin: str
    customer_gstin: Optional[str]
    total_taxable_value: float
    total_cgst: float
    total_sgst: float
    total_igst: float
    total_cess: float
    grand_total: float
    is_validated: bool
    validation_notes: Optional[str]
    model_config = ConfigDict(from_attributes=True)


# --- RAG & KG SCHEMAS ---
class RagSearchRequest(BaseModel):
    query: str = Field(
        ..., min_length=3, json_schema_extra={"example": "Leather clothing classification"}
    )
    top_k: int = Field(5, ge=1, le=20)
    hsn_code_filter: Optional[str] = None


class StandardizedEvidence(BaseModel):
    source: str
    document: Optional[str] = None
    notification: Optional[str] = None
    date: Optional[str] = None
    title: Optional[str] = None
    excerpt: str
    relevance_score: float = 1.0
    effective_from: str = "2017-07-01"
    effective_to: Optional[str] = None
    effective_period: Optional[str] = "2017-07-01 to Present"
    source_url: str = "https://cbic-gst.gov.in"
    url: Optional[str] = None
    retrieved_at: Optional[str] = None
    metadata: Dict[str, Any] = {}


class RagSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[StandardizedEvidence]


class KgQueryRequest(BaseModel):
    cypher_query: Optional[str] = None
    material: Optional[str] = Field(None, json_schema_extra={"example": "Leather"})
    category: Optional[str] = Field(None, json_schema_extra={"example": "Apparel"})


# --- REPORT SCHEMAS ---
class ComplianceReportResponse(BaseModel):
    total_verifications: int
    total_sales: int
    total_invoices: int
    total_tax_collected: float
    total_cgst: float
    total_sgst: float
    total_igst: float
    compliance_score: float
    model_config = ConfigDict(from_attributes=True)


# --- EXPLAINABLE AI SCHEMAS (PHASE 9/11/12) ---
class ExplainableDecisionInput(BaseModel):
    product_description: str
    product_attributes: Dict[str, Any] = {}
    candidate_hsns: List[Dict[str, Any]] = []
    kg_facts: List[Dict[str, Any]] = []
    retrieved_rag_evidence: List[StandardizedEvidence] = []
    gst_rule_records: List[Dict[str, Any]] = []
    effective_date: str = "2017-07-01"
    system_validation_results: Dict[str, Any] = {}


class ExplainableDecisionOutput(BaseModel):
    product: str
    code_type: str = "HSN"
    selected_code: str
    selected_hsn: str = ""  # Backward compatibility alias
    description: str
    hsn_description: str = ""  # Backward compatibility alias
    gst_rate: float
    classification_confidence: float = 90.0
    tax_confidence: float = 95.0
    evidence_confidence: float = 85.0
    overall_confidence: float = 90.0
    confidence: float = 90.0  # Alias for overall_confidence
    result_state: str = "VERIFIED"
    classification_reason: str
    tax_reason: str
    conditions: List[str] = []
    assumptions: List[str] = []
    evidence: List[StandardizedEvidence] = []
    warnings: List[str] = []
    needs_human_review: bool = False
    reconciliation_details: Optional[Dict[str, Any]] = None


# --- ADMIN SCHEMAS ---
class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str]
    action: str
    entity_name: str
    entity_id: Optional[str]
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
