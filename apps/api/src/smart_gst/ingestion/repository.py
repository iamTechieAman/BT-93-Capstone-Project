"""
Ingestion Document Repository.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from smart_gst.ingestion.models import NotificationDocument


class IngestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_number(self, notification_no: str) -> Optional[NotificationDocument]:
        return (
            self.db.query(NotificationDocument)
            .filter(NotificationDocument.notification_no == notification_no)
            .first()
        )

    def list_approved(self) -> List[NotificationDocument]:
        return (
            self.db.query(NotificationDocument)
            .filter(NotificationDocument.status == "APPROVED")
            .all()
        )

    def list_all(self, limit: int = 50, offset: int = 0) -> List[NotificationDocument]:
        return (
            self.db.query(NotificationDocument)
            .order_by(NotificationDocument.fetched_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def update_status(self, notification_no: str, status: str) -> Optional[NotificationDocument]:
        doc = self.get_by_number(notification_no)
        if doc:
            doc.status = status
            self.db.commit()
            self.db.refresh(doc)
        return doc
