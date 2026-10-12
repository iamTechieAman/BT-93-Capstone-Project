"""
Audit Log Database Repository.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from smart_gst.audit.models import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        action: str,
        resource: str,
        role: str = "USER",
        user_id: str = "admin_user",
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        log = AuditLog(
            action=action,
            resource=resource,
            role=role,
            user_id=user_id,
            input_data=input_data,
            output_data=output_data,
            timestamp=datetime.now(timezone.utc),
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list_logs(self, limit: int = 50, offset: int = 0) -> Tuple[List[AuditLog], int]:
        query = self.db.query(AuditLog).order_by(AuditLog.timestamp.desc())
        total = query.count()
        logs = query.offset(offset).limit(limit).all()
        return logs, total
