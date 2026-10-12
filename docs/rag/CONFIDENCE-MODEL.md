# Smart GST Real Multi-Factor Signal-Based Confidence Engine

## 1. Overview & Core Philosophy

The **Real Confidence Engine** ([`backend/app/services/confidence_engine.py`](backend/app/services/confidence_engine.py)) eliminates all hardcoded percentage defaults (`96%`, `95%`, `90%`, `High`). 

Every confidence score is deterministically derived from 10 empirical signals across classification similarity, statutory tax schedule alignment, evidence provenance, and Knowledge Graph ontology validation.

---

## 2. Mathematical Confidence Models

### 1. Overall Confidence Formula

$$\text{overall\_confidence} = 0.40 \cdot C_{\text{classification}} + 0.40 \cdot C_{\text{tax}} + 0.20 \cdot C_{\text{evidence}}$$

Where $C_{\text{classification}}, C_{\text{tax}}, C_{\text{evidence}} \in [0.0, 100.0]$.

---

### 2. Signal Decomposition & Formulas

#### A. Classification Confidence ($C_{\text{classification}}$)
Derived from 4 real classification signals:
1. **Semantic Similarity ($S_{\text{semantic}} \in [0.0, 1.0]$)**: Vector embedding similarity score between product query and HSN tariff descriptions.
2. **Lexical Match ($S_{\text{lexical}} \in [0.0, 1.0]$)**: BM25 token overlap ratio.
3. **Attribute Completeness ($S_{\text{attribute}} \in [0.0, 1.0]$)**: Ratio of extracted product entities (materials, item types, features) present in candidate metadata.
4. **Candidate Ranking Gap ($S_{\text{ranking}} \in [0.0, 1.0]$)**: Margin between top candidate score $s_1$ and 2nd candidate score $s_2$: $S_{\text{ranking}} = \frac{s_1 - s_2}{s_1}$.

$$C_{\text{classification}} = (0.35 \cdot S_{\text{semantic}} + 0.25 \cdot S_{\text{lexical}} + 0.25 \cdot S_{\text{attribute}} + 0.15 \cdot S_{\text{ranking}}) \times 100$$

#### B. Tax Confidence ($C_{\text{tax}}$)
Derived from 3 tax schedule signals:
1. **Rule Match ($S_{\text{rule}} \in [0.0, 1.0]$)**: 1.0 if candidate code matches master CBIC statutory schedule; 0.5 if fallback.
2. **Effective-Date Match ($S_{\text{eff\_date}} \in [0.0, 1.0]$)**: 1.0 if current transaction date falls within $[effective\_from, effective\_to]$; 0.0 if rule is expired.
3. **Contradictory Evidence Penalty ($P_{\text{contradiction}} \in [0.0, 0.5]$)**: Penalty applied if LLM or RAG document proposed a conflicting rate vs statutory schedule rate.

$$C_{\text{tax}} = \max(0.0, 0.50 \cdot S_{\text{rule}} + 0.50 \cdot S_{\text{eff\_date}} - P_{\text{contradiction}}) \times 100$$

#### C. Evidence Confidence ($C_{\text{evidence}}$)
Derived from 3 evidence signals:
1. **Evidence Quality ($S_{\text{quality}} \in [0.0, 1.0]$)**: Average relevance score of retrieved RAG chunks.
2. **Number of Supporting Sources ($S_{\text{sources}} \in [0, 3+]$)**: Count of independent supporting sources ($\min(1.0, \frac{\text{count}}{3})$).
3. **Graph Consistency ($S_{\text{graph}} \in [0.0, 1.0]$)**: Ratio of validated Knowledge Graph ontology relationships.

$$C_{\text{evidence}} = (0.40 \cdot S_{\text{quality}} + 0.30 \cdot \min(1.0, \frac{N_{\text{sources}}}{3}) + 0.30 \cdot S_{\text{graph}}) \times 100$$

---

## 3. Official Result State Assignments

The engine deterministically computes one of seven official result states:

| Result State | Determination Condition | Action Required |
| :--- | :--- | :--- |
| `VERIFIED` | $\text{overall\_confidence} \ge 85.0\%$, no conflicts, active rule | Automated instant approval |
| `LIKELY` | $70.0\% \le \text{overall\_confidence} < 85.0\%$, clear top candidate | Approval with evidence package review |
| `AMBIGUOUS` | Ranking gap $< 0.05$ OR $C_{\text{classification}} < 65.0\%$ | `needs_human_review = true` |
| `REVIEW_REQUIRED` | $\text{overall\_confidence} < 70.0\%$ OR injection attempt detected | Mandatory compliance officer audit |
| `SOURCE_UNAVAILABLE` | RAG retrieval returned 0 chunks AND external source down | Fallback to controlled error state |
| `CONFLICT_DETECTED` | LLM or RAG doc proposed conflicting tax rate vs DB schedule | Overridden to statutory rate; review flagged |
| `OUTDATED_RULE` | Effective date of matched GST rule has expired | Flagged for tariff update |

---

## 4. Evidence Audit Package Requirements

Every evidence item delivered by the pipeline ([`EvidenceItem`](backend/app/schemas/gst_schema.py#L21-L34)) must contain:
1. `source`: Statutory body or publisher (e.g. "Central Board of Indirect Taxes and Customs (CBIC)")
2. `document`: Document title (e.g. "Tariff Schedule Chapter 42")
3. `notification`: Gazette notification number (e.g. "Notification No. 1/2017-Central Tax (Rate)")
4. `date`: Publication date (e.g. "2017-06-28")
5. `effective_period`: Effective period string (e.g. "2017-07-01 to Present")
6. `excerpt`: Text snippet from statutory text
7. `url`: Clickable PDF source URL (e.g. `https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf`)
8. `retrieved_at`: ISO timestamp of retrieval
