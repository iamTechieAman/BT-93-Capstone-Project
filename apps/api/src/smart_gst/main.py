"""
FastAPI Application Entrypoint for Smart GST System.
Single unified route layout under /api/v1.
"""

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from smart_gst.admin.router import router as admin_router
from smart_gst.audit.router import router as audit_router
from smart_gst.auth.models import User

# Feature Routers
from smart_gst.auth.router import router as auth_router
from smart_gst.classification.router import router as classify_router
from smart_gst.common.errors import (
    AppException,
    app_exception_handler,
    generic_http_exception_handler,
)
from smart_gst.common.logging import logger, request_id_ctx
from smart_gst.common.security import get_password_hash
from smart_gst.config import settings
from smart_gst.db.base import Base
from smart_gst.db.session import SessionLocal, engine
from smart_gst.gstin.router import router as gstin_router
from smart_gst.ingestion.router import router as ingestion_router
from smart_gst.invoicing.router import router as invoice_router
from smart_gst.rates.models import TariffHierarchy, TariffRateRule
from smart_gst.rates.router import router as rates_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Smart GST System...")
    # Schema creation fallback for local test environments
    if settings.DATABASE_URL.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)

    # Seed initial statutory tariff catalog & hierarchy
    db = SessionLocal()
    try:
        if db.query(TariffRateRule).count() == 0:
            rules = [
                TariffRateRule(
                    id=str(uuid.uuid4()),
                    hsn_code="42031010",
                    description="Articles of apparel and clothing accessories, of leather",
                    rate=18.0,
                    notification_no="1/2017-Central Tax (Rate)",
                    notification_date="2017-06-28",
                    schedule="Schedule III",
                    serial_no="111",
                    effective_from="2017-07-01",
                    source_url="https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
                ),
                TariffRateRule(
                    id=str(uuid.uuid4()),
                    hsn_code="85414011",
                    description="Photovoltaic solar cell panel module",
                    rate=12.0,
                    notification_no="1/2017-Central Tax (Rate)",
                    notification_date="2017-06-28",
                    schedule="Schedule II",
                    serial_no="234",
                    effective_from="2017-07-01",
                    source_url="https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
                ),
                TariffRateRule(
                    id=str(uuid.uuid4()),
                    hsn_code="09011110",
                    description="Raw unroasted organic coffee beans",
                    rate=0.0,
                    notification_no="2/2017-Central Tax (Rate)",
                    notification_date="2017-06-28",
                    schedule="Schedule I",
                    serial_no="45",
                    effective_from="2017-07-01",
                    source_url="https://cbic-gst.gov.in/pdf/Notification2-CGST-Rate.pdf",
                ),
                TariffRateRule(
                    id=str(uuid.uuid4()),
                    hsn_code="99831300",
                    description="Information technology and cloud SaaS software subscription services",
                    rate=18.0,
                    notification_no="11/2017-Central Tax (Rate)",
                    notification_date="2017-06-28",
                    schedule="Schedule III",
                    serial_no="21",
                    effective_from="2017-07-01",
                    source_url="https://cbic-gst.gov.in/pdf/Notification11-CGST-Rate.pdf",
                ),
                TariffRateRule(
                    id=str(uuid.uuid4()),
                    hsn_code="87032391",
                    description="Motor cars and other motor vehicles principally designed for the transport of persons",
                    rate=28.0,
                    notification_no="1/2017-Central Tax (Rate)",
                    notification_date="2017-06-28",
                    schedule="Schedule IV",
                    serial_no="52",
                    effective_from="2017-07-01",
                    source_url="https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
                ),
            ]

            db.add_all(rules)

            hierarchies = [
                TariffHierarchy(
                    code="42", level="chapter", title="Articles of leather", parent_id=None
                ),
                TariffHierarchy(
                    code="4203",
                    level="heading",
                    title="Articles of apparel and clothing accessories",
                    parent_id="42",
                ),
                TariffHierarchy(
                    code="420310",
                    level="sub_heading",
                    title="Articles of apparel",
                    parent_id="4203",
                ),
                TariffHierarchy(
                    code="42031010",
                    level="tariff_item",
                    title="Jackets and trousers",
                    parent_id="420310",
                ),
                TariffHierarchy(
                    code="85", level="chapter", title="Electrical machinery", parent_id=None
                ),
                TariffHierarchy(
                    code="8541",
                    level="heading",
                    title="Diodes, transistors, solar cells",
                    parent_id="85",
                ),
                TariffHierarchy(
                    code="85414011",
                    level="tariff_item",
                    title="Solar cells and photovoltaic modules",
                    parent_id="8541",
                ),
            ]
            db.add_all(hierarchies)
            db.commit()

        if db.query(User).count() == 0:
            admin_user = User(
                email="admin@smartgst.in",
                hashed_password=get_password_hash("AdminPass123!"),
                role="ADMIN",
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

    yield
    logger.info("Shutting down Smart GST System...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", f"req-{uuid.uuid4().hex[:8]}")
    request.state.request_id = req_id
    token = request_id_ctx.set(req_id)
    start_time = time.time()

    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} ({duration_ms}ms)"
        )
        return response
    finally:
        request_id_ctx.reset(token)


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "req-unknown")
    errors = getattr(exc, "errors", lambda: [])()
    first_msg = errors[0].get("msg", "Validation error") if errors else str(exc)
    return JSONResponse(
        status_code=422,
        content={"code": "VALIDATION_ERROR", "message": first_msg, "request_id": request_id},
    )


# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, generic_http_exception_handler)


# Router Inclusions (All under /api/v1)
app.include_router(auth_router)
app.include_router(classify_router)
app.include_router(invoice_router)
app.include_router(gstin_router)
app.include_router(rates_router)
app.include_router(audit_router)
app.include_router(ingestion_router)
app.include_router(admin_router)


# Root Health Check
@app.get("/healthz", tags=["System"])
def health_check():
    db = SessionLocal()
    try:
        rate_rules_count = db.query(TariffRateRule).count()
        if rate_rules_count == 0:
            return {
                "status": "DEGRADED",
                "service": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "environment": settings.ENVIRONMENT,
                "message": "Core tariff rate tables are empty. Ingestion or data sync required.",
            }
        return {
            "status": "HEALTHY",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "rate_rules_count": rate_rules_count,
        }
    except Exception as e:
        return {
            "status": "DEGRADED",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "error": str(e),
        }
    finally:
        db.close()
