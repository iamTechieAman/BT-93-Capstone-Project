# Smart GST Real 8-Stage Verification Pipeline Architecture

## 1. Executive Summary & Core Principles

The **Real 8-Stage Verification Pipeline** ([`backend/app/services/pipeline_service.py`](backend/app/services/pipeline_service.py)) orchestrates multi-agent product classification, tax rate determination, RAG evidence grounding, Knowledge Graph validation, and deterministic reconciliation.

### Core Hard Constraints
1. **No Faked Completions**: Every stage exposes empirical execution telemetry (start time, end time, duration, status, relevant output, error).
2. **Explicit Status Signals**: Valid execution status values are `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `SKIPPED`, and `REVIEW_REQUIRED`.
3. **Degraded & Conflict State Exposure**:
   - If RAG retrieval fails: Status `FAILED` with explicit error detail.
   - If Knowledge Graph query is unavailable: Status `SKIPPED` or `FAILED`.
   - If LLM rate conflicts with DB: Status `CONFLICT_DETECTED` with reconciliation warning.
4. **Interactive Inspection**: Clicking any stage in the UI visualizer ([`PipelineVisualizer.jsx`](src/components/PipelineVisualizer.jsx)) displays full telemetry, timing, and structured relevant outputs.

---

## 2. 8-Stage Pipeline Specification

```
[Stage 1: User Product Description]
       ↓
[Stage 2: Text Pre-processing & Entity Extraction]
       ↓
[Stage 3: HSN/SAC Candidate Retrieval Engine]
       ↓
[Stage 4: RAG Knowledge Retrieval]
       ↓
[Stage 5: Knowledge Graph Validation]
       ↓
[Stage 6: Explainable AI Decision Engine]
       ↓
[Stage 7: GST Rate Verification & Reconciliation]
       ↓
[Stage 8: Confidence + Evidence Validation]
```

### Stage Breakdown

#### Stage 1: User Product Description
- **Description**: Raw product description ingestion, string sanitization, and XSS / prompt injection protection.
- **Relevant Output**: `raw_input`, `sanitized_query`, `char_count`.
- **Status Signals**: `COMPLETED`, `REVIEW_REQUIRED` (if prompt injection attempt detected).

#### Stage 2: Text Pre-processing
- **Description**: Tokenization, lemmatization, and extraction of product materials, item types, features, and qualifiers.
- **Relevant Output**: `tokens`, `extracted_entities` (`materials`, `item_types`, `accessories`, `qualifiers`).
- **Status Signals**: `COMPLETED`.

#### Stage 3: HSN/SAC Candidate Retrieval
- **Description**: Hybrid vector similarity and BM25 token matching over HSN (Goods) and SAC (Services) catalogs.
- **Relevant Output**: `top_candidates_count`, `top_hsn`, `top_chapter`, `top_description`, `match_score`.
- **Status Signals**: `COMPLETED`, `REVIEW_REQUIRED` (if catalog fallback used).

#### Stage 4: RAG Knowledge Retrieval
- **Description**: Grounded search across statutory CBIC Notifications, Circulars, and Advance Rulings.
- **Relevant Output**: `retrieved_chunks_count`, `sources`, `top_excerpt`.
- **Status Signals**: `COMPLETED`, `SKIPPED` (0 chunks returned), `FAILED` (search exception).

#### Stage 5: Knowledge Graph Validation
- **Description**: Neo4j Cypher graph traversal validating `Product  Material  Category  HSN  Rule  Rate` ontology paths.
- **Relevant Output**: `triples_count`, `chapter_validated`, `sample_triples`.
- **Status Signals**: `COMPLETED`, `SKIPPED` (0 triples matched), `FAILED` (graph server unreachable).

#### Stage 6: Explainable AI Decision Engine
- **Description**: Evidence-backed explanation synthesis without exposing internal Chain-of-Thought trajectories.
- **Relevant Output**: `selected_code`, `classification_reason`, `tax_reason`, `conditions`.
- **Status Signals**: `COMPLETED`, `REVIEW_REQUIRED` (if human review flagged).

#### Stage 7: GST Rate Verification
- **Description**: Statutory schedule rate lookup, CGST/SGST/IGST breakdown, Cess calculation, and LLM override check.
- **Relevant Output**: `gst_rate`, `cgst`, `sgst`, `igst`, `cess`, `reconciliation_warnings`.
- **Status Signals**: `COMPLETED`, `CONFLICT_DETECTED` (if LLM tax rate differed from DB rate).

#### Stage 8: Confidence + Evidence Validation
- **Description**: Multi-factor signal confidence computation (`classification_confidence`, `tax_confidence`, `evidence_confidence`, `overall_confidence`) and Evidence Package assembly.
- **Relevant Output**: `overall_confidence`, `classification_confidence`, `tax_confidence`, `evidence_confidence`, `result_state`, `evidence_count`.
- **Status Signals**: `COMPLETED`, `REVIEW_REQUIRED`, `FAILED`.

---

## 3. Telemetry & Data Structures

Each stage is represented by the [`PipelineStage`](backend/app/schemas/gst_schema.py#L36-L46) schema:

```json
{
  "stage_id": 4,
  "name": "RAG Knowledge Retrieval",
  "status": "COMPLETED",
  "start_time": "2026-10-09T02:18:00.012Z",
  "end_time": "2026-10-09T02:18:00.024Z",
  "duration_ms": 12.4,
  "duration": "12.4ms",
  "relevant_output": {
    "retrieved_chunks_count": 2,
    "sources": ["CBIC Notification No. 1/2017-Central Tax (Rate)"],
    "top_excerpt": "Heading 4203 covers articles of apparel of leather. Applicable rate is 18%."
  },
  "error": null
}
```
