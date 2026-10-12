from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict


class NotificationDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    notification_no: str
    title: str
    category: str
    url: str
    sha256_hash: str
    page_count: int
    status: str
    supersedes: Optional[str] = None
    fetched_at: Union[datetime, str]
    metadata_json: Optional[Dict[str, Any]] = None


class ApprovalPayload(BaseModel):
    status: str = "APPROVED"
    reviewer_notes: Optional[str] = None
