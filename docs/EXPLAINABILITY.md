# Evidence-Backed Explainability Specification

## 1. Overview & Terminology Policy

The Smart GST System delivers user-facing **Evidence-Backed Explanations** detailing why a canonical HSN/SAC code and GST rate apply.

> **UI Terminology Standard**: *Internal technical jargon such as "Explainable CoT Rationale" has been replaced in the user interface with user-facing "Evidence-Backed Explanation".*

---

## 2. Structured JSON Output Schema

The Explainable AI Decision Layer ([`backend/app/llm/llm_provider.py`](backend/app/llm/llm_provider.py)) produces validated structured JSON:

```json
{
  "selected_code": "42031010",
  "code_type": "HSN",
  "hsn_description": "Articles of apparel and clothing accessories, of leather - Jackets",
  "gst_rate": 18.0,
  "cgst_rate": 9.0,
  "sgst_rate": 9.0,
  "igst_rate": 18.0,
  "confidence": 96.0,
  "explanation": "Leather biker jackets are classified under HSN 42031010 as articles of apparel of leather. Under CBIC Notification No. 1/2017-Central Tax (Rate), Schedule III, Entry 112, the statutory GST rate is 18%. Alternative heading 6109 (Knitted T-shirts) was rejected due to material composition (Bovine Leather).",
  "conditions": [
    "Standard apparel schedule rate. Excludes articles of fur."
  ],
  "assumptions": [
    "Material is genuine bovine leather with metallic zipper."
  ],
  "evidence": [
    {
      "label": "CBIC Notification No. 1/2017-Central Tax (Rate), Schedule III, Entry 112",
      "detail": "Statutory 18% GST rate for leather apparel under Heading 4203",
      "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf"
    }
  ],
  "warnings": [],
  "needs_human_review": false
}
```

---

## 3. Strict Safety Guardrails

1. **Evidence Grounding**: Explanations MUST cite retrieved evidence objects.
2. **Reconciliation Override**: If the LLM proposes an ungrounded rate, the deterministic reconciler overrides `gst_rate` with the database value.
