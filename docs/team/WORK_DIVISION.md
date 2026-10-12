# WORK_DIVISION.md — Team Work Division & Responsibility Matrix

**Project**: Smart GST Verification and Manufacturing Sales Automation System  
**Capstone Team Breakdown**:

---

##  Team Work Breakdown Structure

### 1. Aman Kumar — Frontend Planning, UI/UX, React, Tailwind
- **Primary Domain**: Client-Side Architecture, Design System, UI Components.
- **Responsibilities**:
  - Implement responsive visual studio in React 18 + TypeScript + Vite + Tailwind CSS.
  - Build interactive 8-stage pipeline visualizer and Knowledge Graph canvas.
  - Develop B2B Invoice Builder UI with print/PDF layout.
  - Integrate Recharts analytics dashboard and TanStack Query state management.
- **Deliverables**: `frontend/src/components/*`, `frontend/src/App.tsx`.

### 2. Aryan Singh — System Architecture, Backend, API, Databases
- **Primary Domain**: Server Architecture, FastAPI Endpoints, PostgreSQL ORM, Docker.
- **Responsibilities**:
  - Design FastAPI REST API routes (`/api/v1/verify`, `/api/v1/invoice`).
  - Configure SQLAlchemy 2.0 models and PostgreSQL `pgvector` database schema.
  - Orchestrate multi-container `docker-compose.yml` environment.
  - Implement security guardrails, prompt injection sanitizers, and audit trace loggers.
- **Deliverables**: `backend/app/main.py`, `backend/app/core/*`, `backend/app/api/*`, `docker-compose.yml`.

### 3. Priyanshu Gupta — RAG Pipeline, Knowledge Graph, Explainability Engine
- **Primary Domain**: Vector Search, Neo4j Graph DB, LLM Provider Abstraction.
- **Responsibilities**:
  - Develop hybrid candidate retrieval engine (TF-IDF + pgvector embeddings).
  - Implement Neo4j Cypher triple validation and ontology graph seed scripts.
  - Create LLM Provider Abstraction layer (supporting Gemini 1.5 Flash and local Ollama).
  - Synthesize explainable Chain-of-Thought (CoT) reasoning for HSN decisions.
- **Deliverables**: `backend/app/rag/*`, `backend/app/knowledge_graph/*`, `backend/app/llm/*`.

### 4. Palak Mandhan — Dataset Collection, Validation, Literature Review & Documentation
- **Primary Domain**: HSN Data Engineering, Legal Notification Schedules, SRS & Capstone Thesis.
- **Responsibilities**:
  - Collect official CBIC HSN tariff schedules (Chapters 01–98) and Central Tax Notifications.
  - Curate ground-truth evaluation datasets for precision testing.
  - Draft project documentation (`SRS.md`, `SYSTEM_ARCHITECTURE.md`, `README.md`, thesis report).
  - Verify effective dates, legal source URLs, and tax rate accuracy across schedules.
- **Deliverables**: `data/*`, `docs/*`, `tests/`.
