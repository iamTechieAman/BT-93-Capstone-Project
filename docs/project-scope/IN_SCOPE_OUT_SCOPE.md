# IN_SCOPE_OUT_SCOPE.md — Project Scope Boundary

**Project**: Smart GST Verification and Manufacturing Sales Automation System

---

## 1. In Scope (CapStone Deliverables)

### 1.1 Core Functional Modules
1. **Natural Language Product Classification**: Accepts queries (e.g. "Leather Jacket with Zip") and returns 4/6-digit HSN codes across Chapters 01–98.
2. **Explainable RAG + Knowledge Graph Pipeline**:
   - Hybrid retrieval (TF-IDF + pgvector embeddings).
   - Neo4j Cypher triple validation.
   - Gemini 1.5 Flash / Ollama CoT reasoning.
3. **GST Tax Rate Calculation**: CGST, SGST, IGST, Compensation Cess, and Reverse Charge (RCM) checks.
4. **B2B Manufacturing Sales & Invoice Builder**: Interactive tax invoice generator with automatic GSTIN state detection and printable PDF layout.
5. **Analytics & Audit Logging**: Recharts visual dashboard, searchable historical log, and JSON/CSV audit trail export.
6. **Security & Validation Guardrails**: Prompt injection defense, untrusted content sanitization, and dual confidence metrics.

---

## 2. Out of Scope (Future Extensions)

1. **Live GST Portal E-Invoicing Integration**: Direct API filing to NIC E-Invoice portal (`einvoice1.gst.gov.in`) with live IRN generation (requires government sandbox credentials).
2. **Automated GSTR-3B Tax Filing**: Automatic bank sync and tax payment gateway integration.
3. **Multi-Currency International Customs Clearance**: Non-INR currency conversion and foreign import duty calculations.
