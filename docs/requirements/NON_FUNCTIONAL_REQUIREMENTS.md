# Non-Functional Requirements Specification

## Non-Functional Requirements Catalog

| Requirement ID | Domain | Requirement Description | Performance / Security Target | Traceable Implementation |
| :--- | :--- | :--- | :--- | :--- |
| **NFR-001** | API Latency | Verification pipeline execution time SHALL complete within 2.0 seconds. | $< 2.0$s latency | [`backend/app/services/pipeline_service.py`](backend/app/services/pipeline_service.py) |
| **NFR-002** | Token Security | Authentication tokens SHALL be cryptographically signed using HMAC-SHA256 and verified against `SECRET_KEY`. | 0 token forgery | [`backend/app/core/security.py`](backend/app/core/security.py) |
| **NFR-003** | Rate Limiting | The API gateway SHALL enforce sliding-window rate limiting of 120 requests per minute per IP address. | 120 req/min | [`backend/app/main.py`](backend/app/main.py) |
| **NFR-004** | Security Headers | All HTTP responses SHALL set `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and HSTS. | Active headers | `backend/app/main.py` |
| **NFR-005** | Responsiveness | The UI SHALL adapt layout seamlessly across 320px to 1920px viewports without horizontal page overflow. | 320px-1920px | [`src/index.css`](src/index.css) |
| **NFR-006** | Zero Hallucination | Tax rates SHALL be deterministically derived from database schedules; LLM rate claims MUST be overridden if conflicting. | 0 hallucinated rates | [`backend/app/services/evidence_validator.py`](backend/app/services/evidence_validator.py) |
| **NFR-007** | Prompt Defense | Raw inputs SHALL be sanitized of jailbreak patterns and RAG documents wrapped in XML tags. | Active defense | `backend/app/core/security.py` |
| **NFR-008** | Accessibility | Interactive UI elements SHALL include ARIA labels, focus rings, keyboard `Enter` triggers, and contrast ratios $\ge 4.5:1$. | WCAG AA compliant | `src/components/GstVerificationStudio.jsx` |
| **NFR-009** | Build Integrity | Production frontend build SHALL compile with 0 TypeScript/CSS errors. | 0 build errors | `npm run build` |
| **NFR-010** | Test Pass Rate | Automated pytest test suite SHALL maintain a 100% pass rate. | 56/56 tests pass | `backend/tests/` |
