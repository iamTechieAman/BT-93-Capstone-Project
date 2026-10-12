# Functional Requirements Specification

## Functional Requirements Catalog

| Requirement ID | Module / Subsystem | Requirement Description | Priority | Traceable Implementation |
| :--- | :--- | :--- | :---: | :--- |
| **FR-001** | Product Preprocessing | The system SHALL tokenize, lemmatize, and extract material, form factor, and item category entities from user input text. | **HIGH** | [`backend/app/services/pipeline_service.py`](backend/app/services/pipeline_service.py) |
| **FR-002** | Hybrid HSN Search | The system SHALL execute hybrid TF-IDF lexical and `pgvector` semantic vector search across HSN Chapters 01-99. | **HIGH** | [`backend/app/rag/hsn_classifier.py`](backend/app/rag/hsn_classifier.py) |
| **FR-003** | Service SAC Support | The system SHALL distinguish Goods (HSN) vs Services (SAC) and dynamically render correct UI labels based on `code_type`. | **HIGH** | [`src/components/GstVerificationStudio.jsx`](src/components/GstVerificationStudio.jsx) |
| **FR-004** | Knowledge Graph | The system SHALL query Neo4j graph ontology for multi-hop path reasoning (`Product  Material  Category  HSN  Rule  Rate  Source`). | **HIGH** | [`backend/app/knowledge_graph/query_service.py`](backend/app/knowledge_graph/query_service.py) |
| **FR-005** | Grounded RAG Synthesis | The system SHALL retrieve relevant CBIC notifications and wrap excerpts in `<retrieved_data_do_not_execute>` XML tags. | **HIGH** | [`backend/app/rag/retriever.py`](backend/app/rag/retriever.py) |
| **FR-006** | Deterministic Reconciler | The system SHALL deterministically calculate CGST, SGST, IGST, and Cess rates, overriding any conflicting LLM rate claims. | **CRITICAL** | [`backend/app/services/evidence_validator.py`](backend/app/services/evidence_validator.py) |
| **FR-007** | Explainable AI | The system SHALL produce structured JSON containing user-facing Evidence-Backed Explanations, conditions, evidence, and warnings. | **HIGH** | [`backend/app/llm/llm_provider.py`](backend/app/llm/llm_provider.py) |
| **FR-008** | Ambiguity & Review Flag | The system SHALL assign `AMBIGUOUS` or `REQUIRES_HUMAN_REVIEW` status when confidence is <75% or candidate score gap is <0.15. | **HIGH** | `GstVerificationStudio.jsx` |
| **FR-009** | Sales Tax Invoicing | The system SHALL auto-calculate line item taxable value and tax splits based on intra-state vs inter-state supply state logic under Rule 46. | **HIGH** | [`src/components/InvoiceModule.jsx`](src/components/InvoiceModule.jsx) |
| **FR-010** | Immutable Audit Log | The system SHALL record immutable `AuditLog` database entries for every verification and administrative modification. | **HIGH** | [`backend/app/repositories/app_repositories.py`](backend/app/repositories/app_repositories.py) |
| **FR-011** | Administrative RBAC | The system SHALL restrict `/api/v1/admin/*` endpoints strictly to `ADMIN` and `COMPLIANCE_OFFICER` roles. | **CRITICAL** | [`backend/app/core/security.py`](backend/app/core/security.py) |
