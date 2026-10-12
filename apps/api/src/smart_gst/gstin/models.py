"""
GSTIN Cache Database Entity.
"""

from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, String

from smart_gst.db.base import Base


class GstinCache(Base):
    __tablename__ = "gstin_cache"

    gstin = Column(String(15), primary_key=True, index=True)
    legal_name = Column(String(255), nullable=True)
    trade_name = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    registration_date = Column(String(50), nullable=True)
    constitution = Column(String(100), nullable=True)
    jurisdiction = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    provider_name = Column(String(100), nullable=True)
    raw_response = Column(JSON, nullable=True)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False)
