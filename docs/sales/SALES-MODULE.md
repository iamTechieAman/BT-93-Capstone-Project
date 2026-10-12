# Sales Entry & Order Management Module Specification

## 1. Executive Summary & Overview

The **Sales Module** ([`backend/app/api/v1/sales.py`](backend/app/api/v1/sales.py)) handles single and multi-item sales order creation, linking verified product catalog items to customer sales records.

---

## 2. Core Capabilities

1. **Product Master Integration**: Pulls verified HSN codes, chapters, and tax rates directly from domain master tables.
2. **Multi-Item Sales Entry**: Supports adding multiple line items per sale with quantity, unit price, discounts, and HSN/SAC classifications.
3. **Deterministic Calculation**: Computes taxable values, CGST, SGST, IGST, and total order amounts deterministically without relying on LLM inference.
4. **Audit Trail Logging**: Records `CREATE_SALE` audit events with user attribution.

---

## 3. Data Schema & Models

- Sales Order Entity: [`Sale`](backend/app/models/database_models.py#L225-L245)
- Line Item Entity: [`SaleItem`](backend/app/models/database_models.py#L248-L265)
- Pydantic Schemas: [`SaleCreateRequest`](backend/app/schemas/app_schemas.py#L181-L186), [`SaleResponse`](backend/app/schemas/app_schemas.py#L189-L198)

---

## 4. Workflows & API Endpoints

- `POST /api/v1/sales`: Creates a new sales order.
- `GET /api/v1/sales`: Lists all confirmed sales orders.
- `GET /api/v1/sales/{id}`: Retrieves specific sales order details with line items.
