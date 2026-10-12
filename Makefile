# Smart GST System Makefile

.PHONY: help install dev test test-backend test-frontend test-e2e lint build migrate seed clean

help:
	@echo "Smart GST System commands:"
	@echo "  make install        Install dependencies for web and API"
	@echo "  make dev            Run Vite frontend development server"
	@echo "  make test           Run all backend and frontend unit/integration tests"
	@echo "  make test-backend   Run FastAPI backend pytest suite"
	@echo "  make test-frontend  Run React vitest suite"
	@echo "  make test-e2e       Run Playwright browser automation tests"
	@echo "  make lint           Run linters across TypeScript and Python"
	@echo "  make build          Build production web bundle"
	@echo "  make migrate        Run database schema migrations"
	@echo "  make seed           Seed database with development sample data"
	@echo "  make clean          Clean build artifacts, caches, and test output"

install:
	npm install
	pip install -e "apps/api[dev]"

dev:
	npm run dev

test: test-backend test-frontend

test-backend:
	PYTHONPATH=apps/api/src python3 -m pytest apps/api/tests

test-frontend:
	npm test

test-e2e:
	npx playwright test

lint:
	npm run lint
	ruff check apps/api

build:
	npm run build

migrate:
	cd apps/api && PYTHONPATH=src python3 -m alembic upgrade head

seed:
	python3 apps/api/seeds/dev_seed.py

clean:
	rm -rf dist apps/web/dist test-results .pytest_cache apps/api/.pytest_cache .mypy_cache .ruff_cache coverage.xml apps/api/coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
