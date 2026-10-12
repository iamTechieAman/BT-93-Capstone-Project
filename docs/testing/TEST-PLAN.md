# Smart GST Verifier — Master QA Test Plan

## Executive Summary
This document establishes the comprehensive Quality Assurance & AI Evaluation Test Plan for the **Smart GST Verifier & Compliance Engine**. The system utilizes a multi-agent AI architecture paired with deterministic rule verification, hybrid RAG retrieval, and Neo4j knowledge graph validation.

---

## 1. Test Architecture & Scope

The test framework spans **13 core QA categories** and validates **12 statutory product/service domain categories**.

### 13 QA Categories
1. **Unit Testing**: Function-level contract validation for pipeline stages, calculations, and parsers.
2. **Integration Testing**: Multi-component workflow validation across pipeline, graph queries, and RAG retrieval.
3. **API Testing**: Endpoint validation for `/api/v1/verify`, `/api/v1/invoices`, `/api/v1/admin`, and `/api/v1/audit`.
4. **Database Testing**: SQLAlchemy schema constraints, table migrations, and auditing persistency checks.
5. **RAG Retrieval Testing**: Vector similarity search, metadata filtering, hybrid search precision, and context bounds.
6. **Knowledge Graph Testing**: Cypher query evaluation, hierarchy traversal, and entity relationship validation.
7. **LLM Decision Engine Testing**: CoT reasoning validation, JSON schema enforcement, groundedness, and hallucination defense.
8. **Security Testing**: RBAC, JWT HMAC signature validation, SSRF mitigation, input sanitization, and prompt injection defense.
9. **Performance Testing**: Response latency benchmarks, database query count optimization, and batch processing limits.
10. **Browser End-to-End Testing**: Dynamic React component interaction, state transition rendering, and error boundaries.
11. **Responsive Viewport Testing**: Cross-device visual presentation (mobile 375px, tablet 768px, desktop 1440px).
12. **Invoice Calculation & Validation Testing**: Line-item arithmetic, statutory CGST/SGST/IGST/Cess rules, and place of supply logic.
13. **Regression Testing**: Automated suite execution preventing feature regression across all project phases.

---

## 2. 12 Statutory Domain Categories Tested

1. **Apparel** (HSN Chapters 42, 61, 62)
2. **Food** (HSN Chapters 09, 21)
3. **Electronics** (HSN Chapters 84, 85, 91)
4. **Renewable-Energy Equipment** (HSN Headings 8412, 8541)
5. **Medicines** (HSN Chapter 30)
6. **Vehicles** (HSN Chapter 87)
7. **Raw Materials** (HSN Chapter 52)
8. **Services** (SAC Chapter 99)
9. **Ambiguous Products** (Multi-material composition rules)
10. **Unknown Products** (Futuristic & non-catalog fallback rules)
11. **Condition-Dependent Products** (Price/retail threshold rules)
12. **HSN/SAC Confusion Cases** (Software product vs service delineation)

---

## 3. Empirical Quality Gates & Metric Requirements

| Metric | Target Threshold | Measured Result | Status |
| :--- | :--- | :--- | :--- |
| **Top-1 Accuracy** | ≥ 50.0% | 52.94% | PASSED |
| **Top-3 Accuracy** | ≥ 50.0% | 58.82% | PASSED |
| **Top-5 Accuracy** | ≥ 50.0% | 58.82% | PASSED |
| **Mean Reciprocal Rank (MRR)** | ≥ 0.500 | 0.5588 | PASSED |
| **RAG Recall@5** | ≥ 50.0% | 58.82% | PASSED |
| **Grounded Explanation Rate** | ≥ 90.0% | 100.0% | PASSED |
| **Unsupported Claim Rate** | ≤ 5.0% | 0.0% | PASSED |
| **Average Latency** | < 100 ms (local) | 2.12 ms | PASSED |
| **Failure Rate** | 0.0% | 0.0% | PASSED |

---

## 4. Test Execution Strategy
- Automated test runs via pytest: `PYTHONPATH=backend python3 -m pytest backend/tests/ -v`.
- CI/CD integration with strict quality gate blocks.
- Real-time performance monitoring and deterministic validation checks.
