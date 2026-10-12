from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class InvoiceLineItemInput(BaseModel):
    product_name: str = Field(..., min_length=1)
    hsn_code: str = Field(..., min_length=2, max_length=10)
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(..., ge=0.0)
    gst_rate: float = Field(..., ge=0.0)
    cess_rate: float = Field(default=0.0, ge=0.0)


class InvoiceCreatePayload(BaseModel):
    invoice_number: str = Field(..., min_length=1)
    invoice_date: str = Field(default="2026-10-09")
    supplier_gstin: str = Field(..., min_length=15, max_length=15)
    buyer_gstin: str = Field(..., min_length=15, max_length=15)
    place_of_supply: Optional[str] = None
    line_items: List[InvoiceLineItemInput] = Field(..., min_length=1)
    notes: Optional[str] = None


class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_name: str
    hsn_code: str
    quantity: int
    unit_price: float
    taxable_value: float
    gst_rate: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: float
    item_total: float


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    invoice_number: str
    invoice_date: str
    supplier_gstin: str
    buyer_gstin: str
    place_of_supply: str
    status: str
    subtotal: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    grand_total: float
    notes: Optional[str] = None
    created_at: Optional[Union[datetime, str]] = None
    items: List[InvoiceItemResponse] = []
