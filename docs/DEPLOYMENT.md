# Production Deployment & Infrastructure Guide

## 1. Multi-Container Composition

The production deployment uses `docker-compose.yml` to orchestrate 4 services:

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: smart_gst_postgres
    restart: always
    environment:
      POSTGRES_DB: smart_gst_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgrespassword

  neo4j:
    image: neo4j:5-community
    container_name: smart_gst_neo4j
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: smart_gst_backend
    ports:
      - "8000:8000"

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: smart_gst_frontend
    ports:
      - "3000:80"
```

---

## 2. Production Launch Command

```bash
docker-compose up -d --build
```
- Web Client: `http://localhost:3000`
- FastAPI Backend API: `http://localhost:8000`
- Neo4j Browser: `http://localhost:7474`
