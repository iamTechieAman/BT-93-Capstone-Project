"""
Immutable Audit Log Database Entity.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, String

from smart_gst.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default="USER")
    user_id = Column(String(100), nullable=False, default="admin_user")
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
