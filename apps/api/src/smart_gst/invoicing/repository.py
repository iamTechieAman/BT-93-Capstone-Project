"""
Invoice Database Repository.
"""

from typing import List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload

from smart_gst.invoicing.models import Invoice


class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_number(self, invoice_number: str) -> Optional[Invoice]:
        return (
            self.db.query(Invoice)
            .options(joinedload(Invoice.items))
            .filter(Invoice.invoice_number == invoice_number)
            .first()
        )

    def get_by_id(self, invoice_id: str) -> Optional[Invoice]:
        return (
            self.db.query(Invoice)
            .options(joinedload(Invoice.items))
            .filter(Invoice.id == invoice_id)
            .first()
        )

    def list_invoices(self, offset: int = 0, limit: int = 20) -> Tuple[List[Invoice], int]:
        query = (
            self.db.query(Invoice)
            .options(joinedload(Invoice.items))
            .order_by(Invoice.created_at.desc())
        )
        total = query.count()
        items = query.offset(offset).limit(limit).all()
        return items, total

    def create(self, invoice: Invoice) -> Invoice:
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
