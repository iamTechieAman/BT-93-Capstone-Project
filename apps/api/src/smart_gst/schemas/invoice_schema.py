from typing import List

from pydantic import BaseModel


class InvoiceItem(BaseModel):
    description: str
    hsn_code: str
    qty: int
    unit_price: float
    gst_rate: float
    verified: bool = True
    confidence: float = 90.0


class PartyDetails(BaseModel):
    name: str
    gstin: str
    address: str
    state: str


class InvoiceCreateRequest(BaseModel):
    invoice_number: str
    invoice_date: str
    seller: PartyDetails
    buyer: PartyDetails
    items: List[InvoiceItem]


class InvoiceResponse(BaseModel):
    invoice_number: str
    invoice_date: str
    is_inter_state: bool
    subtotal: float
    cgst: float
    sgst: float
    igst: float
    grand_total: float
    status: str = "VALIDATED_AND_ISSUED"
