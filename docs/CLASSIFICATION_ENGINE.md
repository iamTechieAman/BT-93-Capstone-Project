# HSN & SAC Multi-Stage Classification Engine

## 1. Overview & Workflow

The **HSN & SAC Multi-Stage Classification Engine** classifies natural-language product or service trade descriptions into official 8-digit HSN codes (Goods) or 6-digit SAC codes (Services).

```
Trade Description Input
        ↓
1. Text Preprocessing & Entity Extraction (Materials, Form, Category)
        ↓
2. Hybrid Vector Search (TF-IDF Lexical + pgvector Semantic Embeddings)
        ↓
3. Neo4j Knowledge Graph Ontology Validation
        ↓
4. RAG Evidence Synthesis (CBIC Notifications)
        ↓
5. Explainable LLM Reasoning
        ↓
6. Deterministic Tax Rate Engine Reconciliation
        ↓
7. Classification Status Determination & Ambiguity Detection
```

---

## 2. Classification Status Types

The engine assigns one of five official classification status codes:

1. `CONFIRMED`: High confidence (>85%), clear evidence, unambiguous match.
2. `LIKELY`: Good confidence (75%-85%), single candidate head.
3. `AMBIGUOUS`: Close classification scores between multiple candidates (score gap < 0.15).
4. `INSUFFICIENT_INFORMATION`: Missing required product attributes (e.g. material composition or end use).
5. `REQUIRES_HUMAN_REVIEW`: Flagged due to low confidence or conflicting rules.

---

## 3. Ambiguity Detection & User Clarification Prompts

When an ambiguous query is detected (e.g. `"Leather jacket"` where material could be genuine bovine leather vs synthetic leather):
- The system returns `classification_status: AMBIGUOUS`.
- Prompts the user with clarifying questions:
  - *Is the material genuine leather or synthetic leather?*
  - *Is it intended for commercial apparel or protective gear?*
  - *What is the transaction date?*
- Forces human compliance review rather than returning an ungrounded guess.
