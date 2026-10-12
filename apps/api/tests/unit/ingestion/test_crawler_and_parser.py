"""
Unit tests for Ingestion Worker, Parser, and Hasher Isolation.
"""

from smart_gst.workers.hasher import compute_sha256
from smart_gst.workers.parser import IngestionRow, parse_schedule_row


def test_pure_sha256_hasher_isolation():
    data = b"CBIC Central Tax Rate Notification 01/2017"
    h1 = compute_sha256(data)
    h2 = compute_sha256(data)
    assert len(h1) == 64
    assert h1 == h2
    assert compute_sha256(b"Different data") != h1


def test_parser_schedule_row_extraction():
    raw_row = {
        "notification_no": "1/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "schedule": "Schedule III",
        "serial_no": "111",
        "hsn_code": "42031010",
        "description": "Articles of apparel and clothing accessories, of leather",
        "rate": 18.0,
        "effective_from": "2017-07-01",
        "page_number": 12,
        "parse_confidence": 0.95,
    }
    parsed = parse_schedule_row(raw_row)
    assert isinstance(parsed, IngestionRow)
    assert parsed.hsn_code == "42031010"
    assert parsed.rate == 18.0
    assert parsed.status == "approved"
