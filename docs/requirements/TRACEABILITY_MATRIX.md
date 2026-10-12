# Requirements Traceability Matrix (RTM)

## Traceability Mapping: Requirement  Implementation  Test Case  Verification Result

| Requirement ID | Requirement Description | Implementation Module | Automated Test Case | Verification Result |
| :--- | :--- | :--- | :--- | :---: |
| **FR-001** | Product Preprocessing & Entity Extraction | [`backend/app/services/pipeline_service.py`](backend/app/services/pipeline_service.py) | `test_end_to_end_pipeline.py::test_e2e_leather_jacket_verification` |  PASSED |
| **FR-002** | Hybrid HSN Vector Search | [`backend/app/rag/hsn_classifier.py`](backend/app/rag/hsn_classifier.py) | `test_hsn_classifier.py::test_hsn_classifier_leather_jacket` |  PASSED |
| **FR-003** | Service SAC Code Support | [`src/components/GstVerificationStudio.jsx`](src/components/GstVerificationStudio.jsx) | Visual & Unit Component Test |  PASSED |
| **FR-004** | Knowledge Graph Path Traversal | [`backend/app/knowledge_graph/query_service.py`](backend/app/knowledge_graph/query_service.py) | `test_knowledge_graph.py::test_kg_reasoning_path_traversal` |  PASSED |
| **FR-005** | Grounded RAG Document Synthesis | [`backend/app/rag/retriever.py`](backend/app/rag/retriever.py) | `test_rag_pipeline.py::test_rag_retriever_query` |  PASSED |
| **FR-006** | Deterministic Tax Rate Reconciliation | [`backend/app/services/evidence_validator.py`](backend/app/services/evidence_validator.py) | `test_explainable_ai.py::test_explainable_ai_reconciliation` |  PASSED |
| **FR-007** | Explainable AI Rationale | [`backend/app/llm/llm_provider.py`](backend/app/llm/llm_provider.py) | `test_explainable_ai.py::test_structured_json_generation` |  PASSED |
| **FR-008** | Ambiguity & Review Flag | `GstVerificationStudio.jsx` | `test_verify.py::test_verify_endpoint_ambiguity` |  PASSED |
| **FR-009** | Rule 46 Sales Invoicing | [`src/components/InvoiceModule.jsx`](src/components/InvoiceModule.jsx) | `test_sales_and_invoices.py::test_invoice_tax_calculation` |  PASSED |
| **FR-010** | Immutable Audit Trail Logging | [`backend/app/repositories/app_repositories.py`](backend/app/repositories/app_repositories.py) | `test_admin_governance.py::test_audit_log_created_on_data_modification` |  PASSED |
| **FR-011** | Administrative RBAC Enforcement | [`backend/app/core/security.py`](backend/app/core/security.py) | `test_admin_governance.py::test_rbac_forbidden_for_regular_user` |  PASSED |
| **NFR-002**| HMAC JWT Signature Validation | `backend/app/core/security.py` | `test_security_audit.py::test_authentication_rejects_forged_token_signature` |  PASSED |
| **NFR-004**| Security Response Headers | [`backend/app/main.py`](backend/app/main.py) | `test_security_audit.py::test_security_headers_present` |  PASSED |
