"""
Invoice and InvoiceItem Database Entities.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from smart_gst.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    invoice_date = Column(String(50), nullable=False)
    supplier_gstin = Column(String(15), nullable=False)
    buyer_gstin = Column(String(15), nullable=False)
    place_of_supply = Column(String(50), nullable=False)
    status = Column(String(50), default="FINALIZED", nullable=False)
    subtotal = Column(Float, nullable=False)
    cgst_total = Column(Float, default=0.0, nullable=False)
    sgst_total = Column(Float, default=0.0, nullable=False)
    igst_total = Column(Float, default=0.0, nullable=False)
    cess_total = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    hsn_code = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    taxable_value = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    cgst_amount = Column(Float, default=0.0, nullable=False)
    sgst_amount = Column(Float, default=0.0, nullable=False)
    igst_amount = Column(Float, default=0.0, nullable=False)
    cess_amount = Column(Float, default=0.0, nullable=False)
    item_total = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
