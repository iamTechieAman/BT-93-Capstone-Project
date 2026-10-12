"""
Integration tests for Ingestion Document Registry API endpoints (/api/v1/ingestion/*).
"""

from smart_gst.ingestion.models import NotificationDocument


def test_ingestion_documents_list(client, db_session):
    doc = NotificationDocument(
        id="doc_101",
        notification_no="1/2017-Central Tax (Rate)",
        title="Tariff Schedule Notifications",
        category="Central Tax",
        url="https://cbic-gst.gov.in/pdf/notif1.pdf",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        status="APPROVED",
    )
    db_session.add(doc)
    db_session.commit()

    response = client.get("/api/v1/ingestion/documents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["notification_no"] == "1/2017-Central Tax (Rate)"
    assert data[0]["status"] == "APPROVED"
