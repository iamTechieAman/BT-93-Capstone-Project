# Authoritative Source Registry & Ingestion Policy

## 1. Hierarchy of Source Authorities

The system prioritizes tax data sources strictly in order of legal authority:

| Authority Tier | Source Authority Name | Document Types | Primary Domain |
| :---: | :--- | :--- | :--- |
| **Tier 1** | Central Board of Indirect Taxes and Customs (CBIC) | Central Tax Notifications, Circulars, Tariff Schedules | `cbic-gst.gov.in` |
| **Tier 2** | GST Council | Council Meeting Recommendations & Rate Schedules | `gstcouncil.gov.in` |
| **Tier 3** | Official Gazette of India | Statutory Gazette Notifications & Acts | `egazette.gov.in` |
| **Tier 4** | Authority for Advance Rulings (AAR) | State & National Advance Rulings | `gst.gov.in` |

> **Strict Rule**: *Secondary commercial blogs or third-party summaries are strictly forbidden as primary sources of truth. They may only be used for discovery and cross-validation against Tier 1 CBIC documents.*

---

## 2. Source Document Ingestion Registry

All ingested documents retain a unique `source_id` in the database repository ([`backend/app/models/database_models.py`](backend/app/models/database_models.py)):

| Source ID | Notification / Document Title | Authority | Effective Date | Citation Link |
| :--- | :--- | :---: | :---: | :--- |
| `DOC-CBIC-01-2017` | CBIC Notification No. 1/2017-Central Tax (Rate), Schedule III | CBIC | 2017-07-01 | [Notification 1/2017](https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf) |
| `DOC-CBIC-08-2021` | CBIC Notification No. 8/2021-Central Tax (Rate) | CBIC | 2021-10-01 | [Notification 8/2021](https://cbic-gst.gov.in/pdf/Notification8-CGST-Rate.pdf) |
| `DOC-CBIC-02-2017` | CBIC Notification No. 2/2017-Central Tax (Rate), Schedule Nil | CBIC | 2017-07-01 | [Notification 2/2017](https://cbic-gst.gov.in/pdf/Notification2-CGST-Rate.pdf) |
| `DOC-CBIC-11-2017` | CBIC Notification No. 11/2017-Central Tax (Rate) (Services SAC) | CBIC | 2017-07-01 | [Notification 11/2017](https://cbic-gst.gov.in/pdf/Notification11-CGST-Rate.pdf) |

---

## 3. Scraper & Ingestion Policy (Scrapling Guidelines)

When using dynamic source scrapers:
1. Store retrieval timestamp, target URL, HTTP status, and document SHA256 content hash.
2. If the upstream CBIC site is unavailable or scraping fails, the system fails closed gracefully:
   `"Source unavailable / verification required"`
3. Content is sanitized before embedding or ingestion into the RAG vector store.
