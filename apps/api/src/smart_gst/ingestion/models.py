"""
CBIC Notification and Ingestion Document Database Models.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Integer, String

from smart_gst.db.base import Base


class NotificationDocument(Base):
    __tablename__ = "notification_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_no = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # Central Tax, Integrated Tax, Cess
    url = Column(String(500), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    page_count = Column(Integer, default=1, nullable=False)
    status = Column(
        String(50), default="APPROVED", nullable=False
    )  # PENDING_REVIEW, APPROVED, SUPERSEDED
    supersedes = Column(String(100), nullable=True)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    metadata_json = Column(JSON, nullable=True)
