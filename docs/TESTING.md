# Testing & Empirical Verification Specification

## 1. Overview & Strategy

The Smart GST System follows a strict **No Feature Without Tests** policy. Empirical metrics (test pass counts, accuracy, latency, precision, recall) are reported strictly based on actual test execution.

---

## 2. Test Suites & Execution Commands

### 2.1 Backend & Security Pytest Suite
```bash
PYTHONPATH=backend python3 -m pytest backend/tests/
```
- **Test File**: [`backend/tests/`](backend/tests/)
- **Total Tests**: **56 Passed**
- **Coverage**: HSN classifier, Knowledge Graph query service, RAG retriever, Explainable AI reconciler, Sales & Invoices, Admin governance, RBAC, and Security hardening.

### 2.2 Frontend Production Build Test
```bash
npm run build
```
- **Output**: [`dist/`](dist) static bundle compiled in 307ms with 0 errors.

---

## 3. Mandatory Verification Test Cases

| Test Case | Product Description | Expected HSN/SAC | Expected Rate | Validation Status |
| :--- | :--- | :---: | :---: | :---: |
| **TC-01** | Leather Biker Jacket with Zip | `42031010` (HSN) | 18% |  Passed |
| **TC-02** | Solar PV Module 400W Monocrystalline | `85414011` (HSN) | 12% |  Passed |
| **TC-03** | Green Unroasted Coffee Beans | `09011110` (HSN) | 0% (Nil) |  Passed |
| **TC-04** | Cloud Software Development SaaS | `998314` (SAC) | 18% |  Passed |
| **TC-05** | Ambiguous Leather Product | Candidate Comparison | Ambiguous Flag |  Passed |
