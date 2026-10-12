# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-12

### Added
- Modular monorepo architecture with `apps/api` (FastAPI) and `apps/web` (React, TypeScript, Vite).
- Statutory HSN / SAC classification engine with multi-signal evidence evaluation against CBIC tariff schedules.
- Deterministic tax calculation engine enforcing Python `Decimal` arithmetic with `ROUND_HALF_UP` precision for intra-state and inter-state GST.
- Offline and live GSTIN verification pipeline with Modulus-36 checksum calculation and state code verification.
- Rule 46 compliant statutory tax invoice generation and draft finalization workflow.
- Tamper-evident audit logging for classification decisions, GSTIN lookups, and invoice modifications with CSV/JSON export.
- Relational tariff schedule browser with interactive taxonomy hierarchy drawer.
- Data synchronization dashboard for CBIC statutory schedules with content hashing.
- Comprehensive test suite including 73 backend unit/integration tests and 16 frontend component/format tests.
- Docker multi-container compose configuration with PostgreSQL and pgvector support.
- Continuous Integration workflow with automated linting, typing, testing, and bundle builds.
