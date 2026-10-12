# Smart GST Verifier — Environment Variables Specification

## Executive Summary
This document specifies all environment configuration parameters, cryptographic secret requirements, database URLs, CORS origins, and API keys for local, staging, and production environments for the **Smart GST Verifier System**.

---

## 1. Environment Variable Reference Matrix

| Variable Name | Category | Type | Default / Example Value | Description | Mandatory in Prod |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `NODE_ENV` | App | String | `production` | Node environment runtime mode (`development`, `staging`, `production`) | **YES** |
| `ENVIRONMENT` | App | String | `production` | Deployment tier environment indicator | **YES** |
| `DEBUG` | App | Boolean | `false` | Enable/disable verbose debug output | **YES** |
| `PORT` | Networking | Integer | `3000` | Frontend web server port | **YES** |
| `BACKEND_PORT` | Networking | Integer | `8000` | FastAPI backend server port | **YES** |
| `VITE_API_URL` | Frontend | URL | `https://api.smartgstverifier.gov.in/api/v1` | Base URL endpoint for backend REST API | **YES** |
| `SECRET_KEY` | Security | String | `[64-char hex string]` | HMAC SHA-256 secret key for signing JWT tokens | **YES (CRITICAL)** |
| `ALGORITHM` | Security | String | `HS256` | JWT signature encryption algorithm | **YES** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Security | Integer | `480` | JWT token lifetime (in minutes) | **YES** |
| `POSTGRES_HOST` | Database | String | `postgres` | PostgreSQL server hostname | **YES** |
| `POSTGRES_PORT` | Database | Integer | `5432` | PostgreSQL database port | **YES** |
| `POSTGRES_DB` | Database | String | `smart_gst_db` | Primary database name | **YES** |
| `POSTGRES_USER` | Database | String | `smart_gst_user` | Database user account | **YES** |
| `POSTGRES_PASSWORD` | Database | String | `[Secure password]` | Database password credential | **YES (CRITICAL)** |
| `DATABASE_URL` | Database | URL | `postgresql://user:pass@host:5432/db` | SQLAlchemy database connection string | **YES** |
| `NEO4J_URI` | Database | URI | `bolt://neo4j:7687` | Neo4j Bolt protocol URI | **YES** |
| `NEO4J_USER` | Database | String | `neo4j` | Neo4j graph database username | **YES** |
| `NEO4J_PASSWORD` | Database | String | `[Secure password]` | Neo4j graph database password | **YES (CRITICAL)** |
| `LLM_PROVIDER` | AI Engine | String | `gemini` | LLM provider adapter (`gemini`, `ollama`, `mock`) | **YES** |
| `GEMINI_API_KEY` | AI Engine | Secret | `AIzaSy...` | Google Gemini Pro API key | **YES** |
| `OLLAMA_BASE_URL` | AI Engine | URL | `http://ollama:11434` | Local Ollama LLM server endpoint | Optional |
| `ALLOWED_ORIGINS` | Security | CSV | `https://smartgstverifier.gov.in` | CORS allowed origin domains | **YES (CRITICAL)** |
| `RATE_LIMIT_PER_MINUTE` | Security | Integer | `100` | IP rate limit max requests per minute | **YES** |
| `LOG_LEVEL` | Logging | String | `INFO` | Application log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | **YES** |

---

## 2. Cryptographic Secret Management Rules

1. **Zero Secret Commitment**: Never commit `.env`, private keys, API tokens, or production passwords to Git version control. `.env` is listed in `.gitignore`.
2. **Secret Generation**: Production `SECRET_KEY` must be generated using cryptographically secure random bytes:
   ```bash
   openssl rand -hex 32
   ```
3. **Secret Storage**: In production deployments, store secrets in cloud secrets managers (AWS Secrets Manager, GCP Secret Manager, or HashiCorp Vault) and inject as environment variables at container startup.
