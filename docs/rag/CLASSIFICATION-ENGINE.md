# Smart GST HSN/SAC Classification Engine Architecture

## 1. Executive Summary

The **Smart GST Classification Engine** ([`backend/app/rag/hsn_classifier.py`](backend/app/rag/hsn_classifier.py)) is an explainable, multi-stage hybrid classifier designed to classify natural-language trade product and service descriptions into canonical **Harmonized System of Nomenclature (HSN)** codes for Goods and **Services Accounting Codes (SAC)** for Services.

### Core Classification Principles
1. **Goods vs. Services Distinction**: Goods are classified into 8-digit HSN codes (`code_type = "HSN"`), while Services are classified into 6-digit SAC codes (`code_type = "SAC"` under Chapter 99). Service codes are strictly distinguished and never labeled as HSN.
2. **Deterministic Master Catalog Grounding**: Candidates are retrieved exclusively from authoritative CBIC master datasets. The engine never hallucinates non-existent tariff codes.
3. **Attribute-Driven Ambiguity Resolution**: For ambiguous input queries (e.g., generic product descriptions lacking composition or form factor details), the engine prompts for missing attributes rather than making unfounded guesses.

---

## 2. 11-Stage Classification Pipeline Architecture

```
User Query Input
  ↓
Stage 1: Normalization (Lowercasing, Punctuation Stripping, Noise Removal)
  ↓
Stage 2: Tokenization (Stopword Filtering, N-gram Extraction)
  ↓
Stage 3: Entity Extraction (Materials: Leather/Cotton/Silicon; Items: Jacket/Panel/Software)
  ↓
Stage 4: Attribute Extraction (Form factor, composition, unit price thresholds)
  ↓
Stage 5: Candidate Retrieval (Filtering master database by HSN vs SAC taxonomy)
  ↓
Stage 6: Semantic Similarity (Character N-gram Vector Cosine Distance)
  ↓
Stage 7: Lexical Matching (BM25 Keyword & Token Overlap Scoring)
  ↓
Stage 8: Candidate Ranking (Unified Weighted Formula: 0.35 Lexical + 0.35 Semantic + 0.20 Attribute Bonus + 0.10 Type Alignment)
  ↓
Stage 9: Graph Validation (Cross-checking Neo4j material/category constraints)
  ↓
Stage 10: Rule Matching (Validating tax schedule rules & exemption conditions)
  ↓
Stage 11: Final Candidate Set & Status Determination (CONFIRMED / LIKELY / AMBIGUOUS / INSUFFICIENT_INFORMATION / REQUIRES_HUMAN_REVIEW)
```

---

## 3. Classification State Taxonomy

| State | Score Threshold | Criteria & Behavior |
| :--- | :--- | :--- |
| `CONFIRMED` | Match Score $\ge 0.80$, Margin $\ge 0.12$ | Clear match with explicit entity and attribute alignment. High certainty. |
| `LIKELY` | Match Score $\ge 0.65$ | High score, minor ambiguity or alternative heading candidate available. |
| `AMBIGUOUS` | Margin $< 0.08$ between top 2 candidates OR missing key material attribute | Close scores between candidates or underspecified input. Prompts user for missing attributes in `warnings`. |
| `INSUFFICIENT_INFORMATION` | Query Tokens $< 2$ | Extremely short or meaningless input text. Request detailed description. |
| `REQUIRES_HUMAN_REVIEW` | Match Score $< 0.60$ | Low confidence score or rule mismatch. Requires human compliance audit. |

---

## 4. API Request & Response Schema

```json
{
  "classification_status": "AMBIGUOUS",
  "code_type": "HSN",
  "selected_code": "42031010",
  "description": "Articles of apparel and clothing accessories, of leather or of composition leather - Jackets and blazers",
  "matched_attributes": ["material: leather", "term: jacket"],
  "classification_confidence": 78.5,
  "evidence_ids": ["CBIC Notification No. 1/2017-Central Tax (Rate)"],
  "warnings": [
    "Ambiguous product query: Please specify material composition (e.g., genuine bovine leather, woven cotton, or synthetic polyester) to distinguish between HSN 4203, 6203, or 6109."
  ],
  "needs_human_review": true
}
```
