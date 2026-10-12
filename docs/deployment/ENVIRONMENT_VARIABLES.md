# Environment Variables & Configuration Catalog

## 1. Overview

This document catalogs all environment variables used by the **Smart GST Verifier & Compliance Engine** across backend, frontend, database, and container orchestration layers.

---

## 2. Environment Variables Catalog

| Variable Name | Required | Default Value | Description / Security Guidance |
| :--- | :---: | :--- | :--- |
| `NODE_ENV` | Optional | `development` | Environment mode (`development`, `production`, `test`). |
| `PORT` | Optional | `3000` | Port served by frontend Nginx container. |
| `BACKEND_PORT` | Optional | `8000` | Port served by FastAPI backend Uvicorn worker. |
| `VITE_API_URL` | Optional | `/api/v1` | Base API URL used by React frontend client. |
| `SECRET_KEY` | **CRITICAL** | `smart_gst_secret_key_2026` | 64-char random string used for HMAC-SHA256 JWT signature verification. |
| `POSTGRES_USER` | Mandatory | `postgres` | Username for PostgreSQL container. |
| `POSTGRES_PASSWORD` | **CRITICAL** | `postgrespassword` | Password for PostgreSQL container. Must be changed in production. |
| `POSTGRES_HOST` | Mandatory | `localhost` | Host address of PostgreSQL server (`postgres` in Docker Compose). |
| `POSTGRES_PORT` | Mandatory | `5432` | Port of PostgreSQL server. |
| `POSTGRES_DB` | Mandatory | `smart_gst_db` | Name of PostgreSQL database. |
| `NEO4J_URI` | Mandatory | `bolt://localhost:7687` | Bolt protocol URI for Neo4j Knowledge Graph database connection. |
| `NEO4J_USER` | Mandatory | `neo4j` | Username for Neo4j database authentication. |
| `NEO4J_PASSWORD` | **CRITICAL** | `password123` | Password for Neo4j database authentication. Must be changed in production. |
| `GEMINI_API_KEY` | Mandatory | `""` (Empty string) | Google Gemini API key for Explainable AI Chain-of-Thought reasoning. |
| `ALLOWED_ORIGINS` | Optional | `http://localhost:3000` | Comma-separated list of allowed CORS origin URLs. |

---

## 3. Secret Management Guidelines

1. **Zero Secret Commits**:
   - Secrets (`.env`) MUST NOT be committed to git repositories (`.gitignore` ignores `.env`).
2. **Production Secret Injection**:
   - In AWS/GCP or Kubernetes, inject secrets via secret manager stores (e.g. AWS Secrets Manager, HashiCorp Vault, K8s Secrets).
3. **Key Rotation**:
   - Rotate `SECRET_KEY` and `GEMINI_API_KEY` every 90 days.
