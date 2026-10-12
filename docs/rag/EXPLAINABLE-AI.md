# Explainable AI & Evidence-Backed Reasoning Architecture

## 1. Executive Summary & Design Principles

The **Explainable AI Decision Layer** ([`backend/app/llm/explainable_engine.py`](backend/app/llm/explainable_engine.py)) provides verifiable, transparent explanations for product classification and GST rate determination.

### Core Safeguards & Hard Constraints
1. **Zero Chain-of-Thought Exposure**: Internal model thought trajectories are strictly hidden. The UI displays clean **Evidence-Backed Explanations** citing statutory CBIC entries and Knowledge Graph relationships.
2. **LLM is NOT Source of Truth**: The LLM operates as a natural language reasoning generator over supplied evidence. Legal and tax facts are deterministically validated against authoritative database schedules.
3. **Untrusted Data Boundary**: Retrieved documents and user inputs are treated as `UNTRUSTED DATA` wrapped in `<retrieved_data_do_not_execute>` sandboxes to defend against prompt injection and instruction hijacking.

---

## 2. Multi-Context Information Flow

```
1. Product Attributes ───┐
2. HSN/SAC Candidates ───┤
3. KG Graph Facts ────────┼── Prompt Injection Sandbox ── LLM Inference Engine ── Raw Response
4. Retrieved Evidence ───┤
5. GST Rule Schedules ───┤
6. Effective Dates ──────┤
7. Validation Rules ─────┘
```

---

## 3. Structured JSON Response Schema

```json
{
  "product": "Leather Jacket with Zip",
  "code_type": "HSN",
  "selected_code": "42031010",
  "description": "Articles of apparel and clothing accessories, of leather or of composition leather - Jackets and blazers",
  "gst_rate": 18.0,
  "confidence": 0.94,
  "classification_reason": "The item 'Leather Jacket with Zip' is classified under HSN code 42031010. Primary material identification confirms bovine leather construction. Under General Rules of Interpretation (GRI 1 & 3a), articles of leather apparel take precedence over lining materials.",
  "tax_reason": "Statutory GST rate of 18.0% (CGST 9.0% + SGST 9.0%) applies under CBIC Notification No. 1/2017-Central Tax (Rate), Schedule III.",
  "conditions": [
    "Standard apparel schedule rate. Excludes articles of fur (heading 4303)."
  ],
  "assumptions": [
    "Supplied in standard B2B/B2C commercial transaction without special SEZ exemption."
  ],
  "evidence": [
    {
      "source": "CBIC Notification No. 1/2017-Central Tax (Rate)",
      "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
      "title": "Central Tax Rate Schedule - Chapter 42",
      "excerpt": "Heading 4203 applies to articles of apparel and clothing accessories of leather. Standard GST rate is 18%.",
      "relevance_score": 0.92,
      "effective_from": "2017-07-01",
      "effective_to": null,
      "metadata": {
        "hsn_code": "42031010",
        "schedule": "III"
      }
    }
  ],
  "warnings": [],
  "needs_human_review": false
}
```

---

## 4. Post-LLM Deterministic Validation Pipeline

```
Raw LLM JSON Output
  ↓
Stage 1: Schema Validation (Pydantic type safety & required field verification)
  ↓
Stage 2: Rule Validation (Verifying selected HSN/SAC code against DB master candidates)
  ↓
Stage 3: Source Validation (Verifying CBIC document citations & URLs)
  ↓
Stage 4: Arithmetic Validation (Verifying CGST + SGST = IGST, percentage bounds)
  ↓
Stage 5: Contradiction Detection (Overriding conflicting tax rates with DB statutory schedule)
  ↓
Final Reconciled Result (ExplainableDecisionOutput)
```
