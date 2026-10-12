"""
Ingestion API Router under /api/v1/ingestion.
The API only reads approved statutory documents.
"""

from typing import List

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from smart_gst.common.errors import NotFoundException
from smart_gst.common.security import require_role
from smart_gst.db.session import get_db
from smart_gst.ingestion.repository import IngestionRepository
from smart_gst.ingestion.schemas import ApprovalPayload, NotificationDocumentResponse

router = APIRouter(prefix="/api/v1/ingestion", tags=["Source Ingestion"])


@router.get("/documents", response_model=List[NotificationDocumentResponse])
def list_documents(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    repo = IngestionRepository(db)
    docs = repo.list_all(limit=limit, offset=offset)
    return [NotificationDocumentResponse.model_validate(d) for d in docs]


@router.post("/approve/{notification_no}", response_model=NotificationDocumentResponse)
def approve_notification(
    notification_no: str = Path(...),
    payload: ApprovalPayload = ApprovalPayload(),
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(["ADMIN"])),
):
    repo = IngestionRepository(db)
    doc = repo.update_status(notification_no, payload.status)
    if not doc:
        raise NotFoundException(f"Notification '{notification_no}' not found.")
    return NotificationDocumentResponse.model_validate(doc)
