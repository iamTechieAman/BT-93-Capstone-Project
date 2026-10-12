"""
Audit Service for Log Querying and CSV/JSON Export Generation.
"""

import csv
import io
import json
from typing import Any, Dict, List, Optional, Tuple

from smart_gst.audit.repository import AuditRepository
from smart_gst.audit.schemas import AuditLogResponse


class AuditService:
    def __init__(self, audit_repo: AuditRepository):
        self.audit_repo = audit_repo

    def get_logs(self, limit: int = 50, offset: int = 0) -> Tuple[List[AuditLogResponse], int]:
        logs, total = self.audit_repo.list_logs(limit=limit, offset=offset)
        res = [AuditLogResponse.model_validate(entry) for entry in logs]
        return res, total

    def export_csv(self) -> str:
        logs, _ = self.audit_repo.list_logs(limit=1000, offset=0)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["ID", "Timestamp", "User", "Role", "Action", "Resource", "Input", "Output"]
        )
        for entry in logs:
            writer.writerow(
                [
                    entry.id,
                    entry.timestamp.isoformat() if entry.timestamp else "",
                    entry.user_id,
                    entry.role,
                    entry.action,
                    entry.resource,
                    json.dumps(entry.input_data) if entry.input_data else "",
                    json.dumps(entry.output_data) if entry.output_data else "",
                ]
            )
        return output.getvalue()

    def export_json(self) -> str:
        logs, _ = self.audit_repo.list_logs(limit=1000, offset=0)
        data = [
            {
                "id": entry.id,
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else "",
                "user_id": entry.user_id,
                "role": entry.role,
                "action": entry.action,
                "resource": entry.resource,
                "input_data": entry.input_data,
                "output_data": entry.output_data,
            }
            for entry in logs
        ]
        return json.dumps(data, indent=2)

    def log_action(
        self,
        action: str,
        resource: str,
        role: str = "USER",
        user_id: str = "system",
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return self.audit_repo.log_action(
            action=action,
            resource=resource,
            role=role,
            user_id=user_id,
            input_data=input_data or kwargs.get("details"),
            output_data=output_data,
        )

    def export_logs(self, format_type: str = "json") -> str:
        if format_type.lower() == "csv":
            return self.export_csv()
        return self.export_json()
