"""
Audit Log API Router under /api/v1/audit.
Protected for ADMIN & AUDITOR roles.
"""

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from smart_gst.audit.repository import AuditRepository
from smart_gst.audit.schemas import AuditLogResponse
from smart_gst.audit.service import AuditService
from smart_gst.common.security import require_role
from smart_gst.db.session import get_db

router = APIRouter(prefix="/api/v1/audit", tags=["Audit Logs"])


@router.get("/logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(["ADMIN", "AUDITOR"])),
):
    service = AuditService(AuditRepository(db))
    logs, _ = service.get_logs(limit=limit, offset=offset)
    return logs


@router.get("/export/csv")
def export_logs_csv(
    db: Session = Depends(get_db), user: dict = Depends(require_role(["ADMIN", "AUDITOR"]))
):
    service = AuditService(AuditRepository(db))
    csv_content = service.export_csv()
    filename = f"gst_audit_log_export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/export/json")
def export_logs_json(
    db: Session = Depends(get_db), user: dict = Depends(require_role(["ADMIN", "AUDITOR"]))
):
    service = AuditService(AuditRepository(db))
    json_content = service.export_json()
    filename = f"gst_audit_log_export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    return Response(
        content=json_content,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/logs/export")
def export_logs(
    format: str = Query(default="json", pattern="^(json|csv)$"),
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(["ADMIN", "AUDITOR"])),
):
    if format.lower() == "csv":
        return export_logs_csv(db=db, user=user)
    return export_logs_json(db=db, user=user)
