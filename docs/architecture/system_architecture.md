# SYSTEM_ARCHITECTURE.md — Smart GST System Architecture

**Project**: Smart GST Verification and Manufacturing Sales Automation System  
**Document Version**: 2.4.0

---

## 1. High-Level Multi-Tier Architecture

```
                               ┌─────────────────────────────────────────┐
                               │     React + TypeScript Frontend UI      │
                               │  (Vite, Tailwind, TanStack Query, Zod)  │
                               └────────────────────┬────────────────────┘
                                                    │ REST API Calls (HTTP / JSON)
                                                    ▼
                               ┌─────────────────────────────────────────┐
                               │         FastAPI Backend Server          │
                               │ (Security Guardrails, Audit Logger)     │
                               └──────┬──────────────────────┬───────────┘
                                      │                      │
                  ┌───────────────────┴──┐                ┌──┴───────────────────┐
                  ▼                      ▼                ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  ┌────────────────────┐
│ PostgreSQL Vector│  │  Neo4j Knowledge │  │ RAG Legal Rules│  │ LLM Provider Engine│
│   (pgvector DB)  │  │   Graph (Cypher) │  │ (Notifications)│  │ (Gemini / Ollama)  │
└──────────────────┘  └──────────────────┘  └───────────────┘  └────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Frontend Architecture (`frontend/`)
- **React 18 + TypeScript**: Strict type safety (`VerificationResponse`, `InvoiceItem`).
- **TanStack Query (React Query v5)**: Asynchronous state management, caching, and background refetching.
- **Zod Validation**: Form schema validation for user input and party GSTIN.
- **Recharts**: GST tax slab distribution and AI confidence visual analytics.

### 2.2 Backend Architecture (`backend/`)
- **FastAPI Core**: Async REST API endpoints (`/api/v1/verify`, `/api/v1/invoice`).
- **Security & Prompt Injection Sanitizer**: Filters prompt injection vectors prior to LLM/Vector search.
- **LLM Abstraction Layer**: Interface supporting Google Gemini API and local Ollama server.
- **Deterministic Evidence Validator**: Validates LLM output JSON against official DB schedules.

### 2.3 Database Tier
- **PostgreSQL + pgvector**: Stores HSN master records, chapter descriptions, dense embeddings, and audit logs.
- **Neo4j Graph Database**: Stores ontological triples connecting products, raw materials, HSN headings, and tax rate nodes.

---

## 3. Security & Safety Architecture

```
User Product Input ──► Input Sanitizer (Regex & Pattern Guard) ──► RAG / KG Retrieval ──► LLM Engine ──► Pydantic Business Logic Validator ──► Verified Response
```

- **Untrusted Input Handling**: Strip markdown code-fence exploits, system instruction overrides, and jailbreak phrases.
- **Deterministic Overrides**: If LLM output tax rate conflicts with official DB schedule rate, backend overrides LLM with DB truth.
