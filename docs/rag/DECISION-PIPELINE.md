# Smart GST End-to-End Decision Pipeline Architecture

## 1. Overview & 8-Stage Multi-Agent Lifecycle

The **Smart GST Verification Engine** orchestrates 8 specialized agents to deliver verifiable, deterministic, and explainable GST classification:

```
[Stage 1: Input Preprocessing & Security Defense]
       ↓
[Stage 2: HSN/SAC Classification Retrieval Engine]
       ↓
[Stage 3: Knowledge Graph Ontology Reasoning]
       ↓
[Stage 4: Grounded RAG Statutory Document Search]
       ↓
[Stage 5: GST Tax Rate & Schedule Agent]
       ↓
[Stage 6: Explainable AI LLM Decision Engine]
       ↓
[Stage 7: Post-LLM Deterministic Validation & Reconciliation]
       ↓
[Stage 8: Evidence Audit & Confidence Scoring Output]
```

---

## 2. Stage Breakdown & Security Boundaries

### Stage 1: Security & Input Sandboxing
- Sanitizes input string against XSS, HTML injection, and prompt injection patterns.
- Extracts entities (materials, item types, accessories, price qualifiers).

### Stage 2: HSN/SAC Candidate Retrieval
- Executes hybrid vector search and BM25 token matching over Goods (HSN) and Services (SAC) master catalogs.

### Stage 3: Knowledge Graph Traversal
- Traverses Neo4j ontology paths: `Product  Material  Category  HSN/SAC  Rule  Rate  Source`.

### Stage 4: Grounded RAG Document Search
- Retrieves relevant statutory CBIC notifications, circulars, and Advance Rulings.

### Stage 5: Statutory Rule & Schedule Match
- Fetches effective tax rate schedules (CGST, SGST, IGST, Cess) and exemption conditions.

### Stage 6: Explainable LLM Reasoning
- Generates evidence-backed explanations without exposing internal Chain-of-Thought trajectories.

### Stage 7: Deterministic Reconciliation
- Executes 6-stage post-LLM validation:
  `Schema Validation  Rule Validation  Source Validation  Arithmetic Validation  Contradiction Detection  Final Result`.

### Stage 8: Evidence Audit & Output
- Compiles the final evidence package with clickable CBIC PDF source links.
