"""
GSTIN Cache Repository for Database Lookups.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from smart_gst.gstin.models import GstinCache


class GstinCacheRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_valid_cache(self, gstin: str) -> Optional[GstinCache]:
        now = datetime.now(timezone.utc)
        return (
            self.db.query(GstinCache)
            .filter(GstinCache.gstin == gstin, GstinCache.expires_at > now)
            .first()
        )

    def set_cache(self, record: GstinCache) -> GstinCache:
        existing = self.db.query(GstinCache).filter(GstinCache.gstin == record.gstin).first()
        if existing:
            self.db.delete(existing)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
