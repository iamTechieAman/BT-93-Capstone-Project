# Smart GST Verifier — Master Production Deployment Guide

## Executive Summary
This guide provides complete operational instructions for deploying the **Smart GST Verifier & Compliance Engine** across local development, staging environments, and production cloud infrastructure.

---

## 1. Local Setup Instructions

### Prerequisites
- Node.js v20+ and npm v10+
- Python 3.12+
- Docker & Docker Compose v2+

### Step-by-Step Local Deployment
1. **Clone & Configure Environment**:
   ```bash
   git clone https://github.com/org/Smart-GST-System.git
   cd Smart-GST-System
   cp .env.example .env
   ```
2. **Start Infrastructure Services (PostgreSQL + Neo4j)**:
   ```bash
   docker-compose up -d postgres neo4j
   ```
3. **Initialize Backend & Seed Database**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   PYTHONPATH=backend python3 backend/app/db/seed.py
   ```
4. **Run Backend REST API**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. **Run Frontend UI**:
   ```bash
   npm install
   npm run dev
   ```
   Access application UI at `http://localhost:5173`.

---

## 2. Staging & Production Setup Instructions

### Containerized Production Stack Deployment
1. **Prepare Environment File**:
   Generate production `.env` file containing real database passwords, `SECRET_KEY`, and `GEMINI_API_KEY`.
2. **Execute Multi-Container Docker Build**:
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```
3. **Verify Container Health**:
   ```bash
   docker-compose ps
   curl -f http://localhost:8000/api/v1/health
   ```

---

## 3. Database Migration Procedures

1. **SQLAlchemy & Alembic Migration Workflow**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "production_schema_v2"
   alembic upgrade head
   ```
2. **Verification of Table Constraints**:
   Verify indices on `verification_audits(timestamp, hsn_code, user_id)` and pgvector vector columns.

---

## 4. RAG Indexing & Knowledge Graph Initialization

### RAG Vector Database Indexing
Execute automated vector embedding generation for CBIC tariff schedules:
```bash
PYTHONPATH=backend python3 backend/app/rag/pipeline.py --ingest
```

### Knowledge Graph Initialization
Seed Neo4j graph nodes and ontology relationships:
```bash
PYTHONPATH=backend python3 backend/app/knowledge_graph/query_service.py --init-ontology
```

---

## 5. Automated Source Ingestion

Run the Scrapling web crawler and content sanitizer to refresh statutory CBIC notifications:
```bash
PYTHONPATH=backend python3 backend/app/ingestion/scrapling_adapter.py --sync
```

---

## 6. Production Backup Strategy

1. **PostgreSQL Database Backup**:
   ```bash
   docker exec -t smart_gst_postgres pg_dump -U smart_gst_user -F c smart_gst_db > /backups/postgres_$(date +%Y%m%d_%H%M%S).dump
   ```
2. **Neo4j Graph Database Backup**:
   ```bash
   docker exec -t smart_gst_neo4j neo4j-admin database dump neo4j --to-path=/backups/neo4j/
   ```
3. **Schedule Automated Daily Cron Job**:
   Configure daily cron backup at 02:00 UTC with 30-day retention policy.

---

## 7. Production Rollback Strategy

1. **Application Container Rollback**:
   ```bash
   docker-compose down
   git checkout tags/v2.3-stable
   docker-compose up -d --build
   ```
2. **Database Schema Rollback**:
   ```bash
   cd backend
   alembic downgrade -1
   ```
3. **Restoring Database Backup**:
   ```bash
   pg_restore -U smart_gst_user -d smart_gst_db /backups/postgres_target.dump
   ```
