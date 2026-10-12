"""
Smart GST System - SQLAlchemy ORM Data Models.
Defines all 15 relational tables required for the GST verification and sales workflow.
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="USER")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)  # AUTHORITATIVE_CBIC, DEMO_SAMPLE
    publisher = Column(String(255), nullable=False, default="CBIC")
    document_url = Column(Text, nullable=False)
    retrieved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    notifications = relationship(
        "Notification", back_populates="source", cascade="all, delete-orphan"
    )


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    notification_number = Column(String(100), nullable=False, unique=True, index=True)
    title = Column(String(500), nullable=False)
    issuing_authority = Column(String(255), nullable=False, default="CBIC")
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    pdf_url = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    source = relationship("Source", back_populates="notifications")
    gst_rates = relationship("GstRate", back_populates="notification")
    gst_rules = relationship("GstRule", back_populates="notification")


class HsnCode(Base):
    __tablename__ = "hsn_codes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    hsn_code = Column(String(10), nullable=False, unique=True, index=True)
    hsn_level = Column(String(20), nullable=False)  # 2-digit, 4-digit, 6-digit, 8-digit
    chapter = Column(String(2), nullable=False, index=True)
    heading = Column(String(4), nullable=True, index=True)
    subheading = Column(String(6), nullable=True, index=True)
    technical_description = Column(Text, nullable=False)
    trade_description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    gst_rates = relationship("GstRate", back_populates="hsn_code", cascade="all, delete-orphan")
    gst_rules = relationship("GstRule", back_populates="hsn_code", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="hsn_code_rel")


class GstRate(Base):
    __tablename__ = "gst_rates"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    hsn_code_id = Column(String(36), ForeignKey("hsn_codes.id", ondelete="CASCADE"), nullable=False)
    notification_id = Column(
        String(36), ForeignKey("notifications.id", ondelete="RESTRICT"), nullable=False
    )
    gst_rate = Column(Float, nullable=False)
    cgst_rate = Column(Float, nullable=False)
    sgst_rate = Column(Float, nullable=False)
    igst_rate = Column(Float, nullable=False)
    cess_rate = Column(Float, nullable=False, default=0.0)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    hsn_code = relationship("HsnCode", back_populates="gst_rates")
    notification = relationship("Notification", back_populates="gst_rates")


class SacCode(Base):
    __tablename__ = "sac_codes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sac_code = Column(String(10), nullable=False, unique=True, index=True)
    chapter = Column(String(2), nullable=False, default="99", index=True)
    heading = Column(String(4), nullable=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, default="Services", index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class GstRule(Base):
    __tablename__ = "gst_rules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    hsn_code_id = Column(String(36), ForeignKey("hsn_codes.id", ondelete="CASCADE"), nullable=False)
    notification_id = Column(
        String(36), ForeignKey("notifications.id", ondelete="RESTRICT"), nullable=False
    )
    rule_name = Column(String(255), nullable=False)
    conditions = Column(Text, nullable=False)
    exceptions = Column(Text, nullable=True)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    hsn_code = relationship("HsnCode", back_populates="gst_rules")
    notification = relationship("Notification", back_populates="gst_rules")


class GstRuleVersion(Base):
    __tablename__ = "gst_rule_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    rule_id = Column(
        String(36), ForeignKey("gst_rules.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number = Column(Integer, nullable=False, default=1)
    rule_name = Column(String(255), nullable=False)
    conditions = Column(Text, nullable=False)
    exceptions = Column(Text, nullable=True)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_name = Column(String(255), nullable=False, index=True)
    product_description = Column(Text, nullable=False)
    material = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    hsn_code_id = Column(String(36), ForeignKey("hsn_codes.id", ondelete="SET NULL"), nullable=True)
    unit_price = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    hsn_code_rel = relationship("HsnCode", back_populates="products")


class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    product_name = Column(String(255), nullable=False)
    product_description = Column(Text, nullable=False)
    declared_hsn = Column(String(10), nullable=True)
    declared_material = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    result = relationship(
        "VerificationResult", back_populates="request", uselist=False, cascade="all, delete-orphan"
    )


class VerificationResult(Base):
    __tablename__ = "verification_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(
        String(36),
        ForeignKey("verification_requests.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    recommended_hsn_id = Column(
        String(36), ForeignKey("hsn_codes.id", ondelete="RESTRICT"), nullable=False
    )
    verified_gst_rate = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    reasoning_summary = Column(Text, nullable=False)
    chain_of_thought = Column(JSON, nullable=False)
    validation_status = Column(String(50), nullable=False, default="VERIFIED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    request = relationship("VerificationRequest", back_populates="result")
    retrieval_chunks = relationship(
        "RetrievalChunk", back_populates="result", cascade="all, delete-orphan"
    )


class RetrievalChunk(Base):
    __tablename__ = "retrieval_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    verification_result_id = Column(
        String(36), ForeignKey("verification_results.id", ondelete="CASCADE"), nullable=False
    )
    source_id = Column(String(36), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    chunk_text = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=False)
    chunk_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    result = relationship("VerificationResult", back_populates="retrieval_chunks")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sale_number = Column(String(100), nullable=False, unique=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_gstin = Column(String(15), nullable=True)
    sale_date = Column(Date, nullable=False, default=date.today)
    status = Column(String(50), nullable=False, default="DRAFT")
    total_amount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="sale", uselist=False)


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sale_id = Column(String(36), ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    hsn_code_id = Column(
        String(36), ForeignKey("hsn_codes.id", ondelete="RESTRICT"), nullable=False
    )
    quantity = Column(Float, nullable=False, default=1.0)
    unit_price = Column(Float, nullable=False)
    taxable_value = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    sale = relationship("Sale", back_populates="items")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sale_id = Column(
        String(36), ForeignKey("sales.id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    invoice_number = Column(String(100), nullable=False, unique=True, index=True)
    invoice_date = Column(Date, nullable=False, default=date.today)
    place_of_supply = Column(String(100), nullable=False)
    supplier_gstin = Column(String(15), nullable=False)
    customer_gstin = Column(String(15), nullable=True)
    total_taxable_value = Column(Float, nullable=False)
    total_cgst = Column(Float, nullable=False)
    total_sgst = Column(Float, nullable=False)
    total_igst = Column(Float, nullable=False)
    total_cess = Column(Float, nullable=False, default=0.0)
    grand_total = Column(Float, nullable=False)
    is_validated = Column(Boolean, nullable=False, default=False)
    validation_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    sale = relationship("Sale", back_populates="invoice")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String(255), nullable=False)
    hsn_code = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    taxable_value = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    cgst_amount = Column(Float, nullable=False)
    sgst_amount = Column(Float, nullable=False)
    igst_amount = Column(Float, nullable=False)
    cess_amount = Column(Float, nullable=False, default=0.0)
    item_total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    invoice = relationship("Invoice", back_populates="items")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    entity_name = Column(String(100), nullable=False)
    entity_id = Column(String(36), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    changes_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class GSTINAuditRecord(Base):
    __tablename__ = "gstin_audit_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_id = Column(String(36), nullable=True)
    gstin = Column(String(15), nullable=False, index=True)
    masked_gstin = Column(String(15), nullable=False)
    format_valid = Column(Boolean, nullable=False)
    structural_valid = Column(Boolean, nullable=False)
    checksum_valid = Column(Boolean, nullable=False)
    registration_verified = Column(Boolean, nullable=False)
    taxpayer_status = Column(String(50), nullable=False)
    verification_status = Column(String(50), nullable=False)
    provider_name = Column(String(100), nullable=False)
    latency_ms = Column(Float, nullable=False, default=0.0)
    cache_hit = Column(Boolean, nullable=False, default=False)
    error_code = Column(String(50), nullable=True)
    response_metadata = Column(JSON, nullable=True)


class GSTINCacheRecord(Base):
    __tablename__ = "gstin_cache_records"

    gstin = Column(String(15), primary_key=True)
    result_json = Column(JSON, nullable=False)
    verified_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    source_name = Column(String(100), nullable=False)
