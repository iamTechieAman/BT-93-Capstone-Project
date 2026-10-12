# Smart GST Grounded RAG Pipeline Architecture

## 1. Overview & Core Design

The **Smart GST RAG Engine** ([`backend/app/rag/pipeline.py`](backend/app/rag/pipeline.py)) implements an end-to-end statutory document retrieval pipeline designed to enforce **Zero Unsupported Claims**. Every answer produced by the system is backed by verifiable, structured evidence citing official CBIC Notifications, Circulars, and Tariff Schedules.

### 13-Stage Production RAG Pipeline Flow
```
Authoritative Source (CBIC PDF / Gazette)
  ↓
Stage 1: Document Loader (Scrapling / Ingestion Adapter)
  ↓
Stage 2: Parsing (PDF Text Extraction / Section Splitting)
  ↓
Stage 3: Cleaning (Whitespace Normalization, Control Character Stripping)
  ↓
Stage 4: Sanitization (Prompt Injection Filtering, Tag Stripping)
  ↓
Stage 5: Chunking (Sliding Window 300 chars, 50 overlap)
  ↓
Stage 6: Metadata Extraction (Document ID, Section, Page, HSN/SAC Code, Notification)
  ↓
Stage 7: Embeddings Generation (Dense N-gram Vector Feature Mapping)
  ↓
Stage 8: Vector Database Indexing (Dense Feature Vectors + Metadata Keys)
  ↓
Stage 9: Retrieval (Hybrid Search: Sparse BM25 + Dense Vector Cosine Similarity)
  ↓
Stage 10: Metadata & Date Range Filtering (Effective Date Range, HSN/SAC Filter)
  ↓
Stage 11: Candidate Code Filtering (Candidate Code Array Match)
  ↓
Stage 12: Reranking & Relevance Thresholding (Excluding scores < 0.20)
  ↓
Stage 13: Evidence Package Generation (Synthesizing StandardizedEvidence Envelope)
```

---

## 2. Chunk Metadata Retention Specification

Every document chunk indexed by the vector engine preserves the following mandatory metadata attributes:

| Metadata Attribute | Type | Description |
| :--- | :--- | :--- |
| `source` | `string` | Authoritative publisher title (e.g. `CBIC Notification No. 1/2017-Central Tax (Rate)`) |
| `source_url` | `string` | Canonical URL link to statutory document PDF |
| `document` / `document_id` | `string` | Unique document identifier (e.g. `CBIC-NOTIF-01-2017-SCHED3`) |
| `title` | `string` | Official document title |
| `page` / `section` | `string / int` | Specific entry page and section (e.g. `Schedule III, Entry 112`, `Page 1`) |
| `code` / `hsn_code` | `string` | Target 8-digit HSN or 6-digit SAC code (e.g. `42031010` or `998313`) |
| `category` | `string` | Functional category classification |
| `effective_from` | `string (ISO Date)`| Statutory start date of notification |
| `effective_to` | `string (ISO Date / null)`| Expiration or sunset date of notification |
| `notification` | `string` | Official CBIC notification reference number |
| `metadata` | `dict` | Additional schedule entries and publisher tags |

---

## 3. Evidence Object Schema

The output of the RAG pipeline strictly adheres to the `StandardizedEvidence` Pydantic schema:

```json
{
  "source": "CBIC Notification No. 1/2017-Central Tax (Rate)",
  "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
  "title": "CBIC Notification No. 1/2017-Central Tax (Rate), Schedule III",
  "excerpt": "Heading 4203 applies to articles of apparel and clothing accessories, of leather or of composition leather. Standard GST rate is 18% (9% CGST + 9% SGST). Excludes articles of fur under heading 4303.",
  "relevance_score": 0.895,
  "effective_from": "2017-07-01",
  "effective_to": null,
  "metadata": {
    "document_id": "CBIC-NOTIF-01-2017-SCHED3",
    "chunk_id": "CBIC-NOTIF-01-2017-SCHED3-S0-C0",
    "section": "Schedule III, Entry 112",
    "page": 1,
    "hsn_code": "42031010",
    "category": "Apparel & Accessories"
  }
}
```
