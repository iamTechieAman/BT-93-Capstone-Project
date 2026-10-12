"""
Invoice Management API Router under /api/v1/invoices.
Protected for ACCOUNTANT and ADMIN roles.
"""

from typing import List

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from smart_gst.common.errors import NotFoundException
from smart_gst.common.security import require_role
from smart_gst.db.session import get_db
from smart_gst.invoicing.repository import InvoiceRepository
from smart_gst.invoicing.schemas import InvoiceCreatePayload, InvoiceResponse
from smart_gst.invoicing.service import TaxDomainService

router = APIRouter(prefix="/api/v1/invoices", tags=["Invoices"])


@router.post("", response_model=InvoiceResponse)
def create_invoice(
    payload: InvoiceCreatePayload,
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(["ADMIN", "ACCOUNTANT"])),
):
    repo = InvoiceRepository(db)
    invoice = TaxDomainService.create_invoice(repo, payload)
    return InvoiceResponse.model_validate(invoice)


@router.get("/{invoice_id_or_number}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id_or_number: str = Path(..., description="Invoice ID or Invoice Number"),
    db: Session = Depends(get_db),
):
    repo = InvoiceRepository(db)
    invoice = repo.get_by_id(invoice_id_or_number) or repo.get_by_number(invoice_id_or_number)
    if not invoice:
        raise NotFoundException(f"Invoice '{invoice_id_or_number}' not found.")
    return InvoiceResponse.model_validate(invoice)


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    repo = InvoiceRepository(db)
    invoices, _ = repo.list_invoices(offset=offset, limit=limit)
    return [InvoiceResponse.model_validate(inv) for inv in invoices]
