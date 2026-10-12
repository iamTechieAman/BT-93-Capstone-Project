# Unified Confidence Model Specification

## 1. Mathematical Formulation

The unified confidence score $C_{\text{final}} \in [0.0, 1.0]$ measures the overall reliability of a GST classification decision.

$$C_{\text{final}} = \text{round}\left(0.40 \cdot C_{\text{class}} + 0.40 \cdot C_{\text{tax}} + 0.20 \cdot C_{\text{ev}}, \; 4\right)$$

---

## 2. Metric Component Breakdown

### 1. Classification Match Score ($C_{\text{class}}$) — Weight: 0.40
Measures candidate match quality from the retrieval & reranking engine:
$$C_{\text{class}} = \min\left(1.0, \max\left(0.0, \text{MatchScore}_{\text{top\_candidate}}\right)\right)$$

### 2. Tax Schedule Verification ($C_{\text{tax}}$) — Weight: 0.40
Measures statutory tax schedule verification in PostgreSQL & CBIC tables:
$$C_{\text{tax}} = \begin{cases} 1.00 & \text{if HSN and GST rate match verified CBIC schedule} \\ 0.50 & \text{otherwise} \end{cases}$$

### 3. Evidence Quality Score ($C_{\text{ev}}$) — Weight: 0.20
Measures completeness of statutory RAG citations and Knowledge Graph triples:
$$C_{\text{ev}} = \begin{cases} 1.00 & \text{if statutory RAG citations AND Knowledge Graph triples exist} \\ 0.80 & \text{if statutory RAG citations exist} \\ 0.50 & \text{otherwise} \end{cases}$$

---

## 3. Human Review Trigger Thresholds

A decision is automatically flagged for human compliance review (`needs_human_review = true`) if:

1. $C_{\text{final}} < 0.75$ (Overall confidence below 75%).
2. Post-LLM deterministic reconciler detected a conflict and executed an override (HSN code or GST rate mismatch).
3. The product description contains ambiguous material combinations (e.g. leather apparel with heavy fur attachments).
