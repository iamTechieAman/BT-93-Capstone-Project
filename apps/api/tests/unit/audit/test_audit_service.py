"""
Unit tests for Audit Service logging and CSV/JSON export.
"""

from smart_gst.audit.repository import AuditRepository
from smart_gst.audit.service import AuditService


def test_audit_log_creation_and_export(db_session):
    repo = AuditRepository(db_session)
    service = AuditService(repo)

    log = service.log_action(
        action="CLASSIFY",
        user_id="compliance@smartgst.in",
        resource="42031010",
        details={"hsn": "42031010", "rate": 18.0},
    )

    assert log.id is not None
    assert log.action == "CLASSIFY"

    json_export = service.export_logs(format_type="json")
    assert "42031010" in json_export

    csv_export = service.export_logs(format_type="csv")
    assert "CLASSIFY" in csv_export
