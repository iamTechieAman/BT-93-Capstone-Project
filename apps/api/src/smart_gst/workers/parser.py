"""
Statutory Schedule and Notification Parser Worker.
"""

from typing import Any, Dict

from pydantic import BaseModel


class IngestionRow(BaseModel):
    notification_no: str
    notification_date: str
    schedule: str
    serial_no: str
    hsn_code: str
    description: str
    rate: float
    effective_from: str
    page_number: int
    parse_confidence: float
    status: str = "approved"


def parse_schedule_row(raw_data: Dict[str, Any]) -> IngestionRow:
    """Parse raw schedule table row into validated IngestionRow."""
    confidence = float(raw_data.get("parse_confidence", 0.90))
    status = "approved" if confidence >= 0.85 else "needs_review"

    return IngestionRow(
        notification_no=str(raw_data.get("notification_no", "")),
        notification_date=str(raw_data.get("notification_date", "")),
        schedule=str(raw_data.get("schedule", "")),
        serial_no=str(raw_data.get("serial_no", "")),
        hsn_code=str(raw_data.get("hsn_code", "")),
        description=str(raw_data.get("description", "")),
        rate=float(raw_data.get("rate", 18.0)),
        effective_from=str(raw_data.get("effective_from", "2017-07-01")),
        page_number=int(raw_data.get("page_number", 1)),
        parse_confidence=confidence,
        status=status,
    )
