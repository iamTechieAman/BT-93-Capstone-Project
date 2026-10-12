# Scrapling Scraper Integration & Adaptive Extraction Specification

## 1. Integration Rationale & Architecture

The `ScraplingAdapter` ([`backend/app/ingestion/scrapling_adapter.py`](backend/app/ingestion/scrapling_adapter.py)) provides an isolated abstraction layer for dynamic web fetching and HTML extraction targeting official CBIC tax notification portals.

---

## 2. Resilience & Hardening Controls

1. **Exponential Backoff & Retries**: Automatically retries failed HTTP requests up to `max_retries = 3` with exponential backoff delays.
2. **Rate Limiting**: Enforces a minimum delay of 0.5s between consecutive requests (`rate_limit_delay`) to comply with governmental web server access policies.
3. **Timeout Handling**: Hard timeout threshold (`timeout_seconds = 5`) per request attempt.
4. **Data vs Instruction Boundaries**: `IngestionSanitizer` strips dangerous prompt injection vectors and encloses extracted text within `<retrieved_data_do_not_execute>` XML tags.
