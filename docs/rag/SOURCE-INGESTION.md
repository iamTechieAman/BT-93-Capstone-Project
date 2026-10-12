# Source Ingestion & Data Provenance Architecture

## 1. Overview & Data Pipeline

The **Source Ingestion Subsystem** ([`backend/app/ingestion/`](backend/app/ingestion/)) manages dynamic document fetching, HTML extraction, data sanitization, content hashing, and provenance storage for the Smart GST System.

```
Authoritative Source URL (e.g. CBIC PDF / HTML)
                       ↓
           Scrapling Scraper Adapter
                       ↓
   Retry / Backoff / Rate Limiting Control
                       ↓
           HTML Content Extraction
                       ↓
        Ingestion Sanitizer & SHA-256 Hashing
                       ↓
  XML Data Boundary Wrapping (<retrieved_data>)
                       ↓
       Grounded RAG Vector Store Indexing
```

---

## 2. Ingested Document Metadata Schema

Every ingested document record maintains provenance metadata:

| Metadata Field | Data Type | Description |
| :--- | :--- | :--- |
| `source_url` | `VARCHAR(500)` | Direct HTTPS URL to statutory publication |
| `source_name` | `VARCHAR(255)` | Publishing authority (e.g. `CBIC`) |
| `retrieved_at` | `TIMESTAMP` | UTC timestamp of ingestion |
| `content_hash` | `VARCHAR(64)` | SHA-256 hash of raw extracted text |
| `document_hash` | `VARCHAR(64)` | SHA-256 hash of document identification metadata |
| `extraction_status` | `VARCHAR(50)` | `COMPLETED`, `SOURCE_UNAVAILABLE`, `TIMED_OUT`, `RATE_LIMITED` |
| `document_title` | `VARCHAR(255)` | Official title or notification number |
| `document_date` | `DATE` | Publication date |

---

## 3. Graceful Fallback Policy

> **Strict Fail-Closed Directive**: *If remote source retrieval fails or times out, the system MUST return `extraction_status = SOURCE_UNAVAILABLE` and prompt for manual compliance verification. The system MUST NEVER generate fake or hallucinated replacement text.*
