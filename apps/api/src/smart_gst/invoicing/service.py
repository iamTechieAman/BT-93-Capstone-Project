"""
Tax Domain Service with Deterministic Decimal Computation and Rule 46 Compliance.
Uses Decimal and ROUND_HALF_UP everywhere to eliminate floating point imprecision.
"""

from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict

from smart_gst.common.errors import ValidationException
from smart_gst.invoicing.models import Invoice, InvoiceItem
from smart_gst.invoicing.repository import InvoiceRepository
from smart_gst.invoicing.schemas import InvoiceCreatePayload


def quantize_currency(value: Decimal) -> Decimal:
    """Quantize to 2 decimal places using standard ROUND_HALF_UP statutory rounding."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class TaxDomainService:
    @staticmethod
    def calculate_line_item(
        quantity: int,
        unit_price: float,
        gst_rate: float,
        is_interstate: bool,
        cess_rate: float = 0.0,
    ) -> Dict[str, Any]:
        qty = Decimal(str(quantity))
        price = Decimal(str(unit_price))
        rate = Decimal(str(gst_rate))
        cess = Decimal(str(cess_rate))
        hundred = Decimal("100")
        two = Decimal("2")

        taxable_value = quantize_currency(qty * price)

        if is_interstate:
            igst_amount = quantize_currency(taxable_value * (rate / hundred))
            cgst_amount = Decimal("0.00")
            sgst_amount = Decimal("0.00")
        else:
            half_rate = rate / two
            cgst_amount = quantize_currency(taxable_value * (half_rate / hundred))
            sgst_amount = quantize_currency(taxable_value * (half_rate / hundred))
            igst_amount = Decimal("0.00")

        cess_amount = (
            quantize_currency(taxable_value * (cess / hundred)) if cess > 0 else Decimal("0.00")
        )
        item_total = quantize_currency(
            taxable_value + cgst_amount + sgst_amount + igst_amount + cess_amount
        )

        return {
            "taxable_value": float(taxable_value),
            "gst_rate": float(rate),
            "cgst_amount": float(cgst_amount),
            "sgst_amount": float(sgst_amount),
            "igst_amount": float(igst_amount),
            "cess_amount": float(cess_amount),
            "item_total": float(item_total),
        }

    @classmethod
    def create_invoice(cls, repo: InvoiceRepository, payload: InvoiceCreatePayload) -> Invoice:
        existing = repo.get_by_number(payload.invoice_number)
        if existing:
            raise ValidationException(
                f"Invoice number '{payload.invoice_number}' already exists.", code="INVOICE_EXISTS"
            )

        seller_state = payload.supplier_gstin[:2] if len(payload.supplier_gstin) >= 2 else "07"
        pos = payload.place_of_supply or payload.buyer_gstin[:2]
        buyer_state = payload.buyer_gstin[:2] if len(payload.buyer_gstin) >= 2 else pos
        is_interstate = seller_state != buyer_state

        subtotal_d = Decimal("0.00")
        cgst_total_d = Decimal("0.00")
        sgst_total_d = Decimal("0.00")
        igst_total_d = Decimal("0.00")
        cess_total_d = Decimal("0.00")

        db_items = []
        for item in payload.line_items:
            calc = cls.calculate_line_item(
                quantity=item.quantity,
                unit_price=item.unit_price,
                gst_rate=item.gst_rate,
                is_interstate=is_interstate,
                cess_rate=item.cess_rate,
            )

            subtotal_d += Decimal(str(calc["taxable_value"]))
            cgst_total_d += Decimal(str(calc["cgst_amount"]))
            sgst_total_d += Decimal(str(calc["sgst_amount"]))
            igst_total_d += Decimal(str(calc["igst_amount"]))
            cess_total_d += Decimal(str(calc["cess_amount"]))

            db_items.append(
                InvoiceItem(
                    product_name=item.product_name,
                    hsn_code=item.hsn_code,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    taxable_value=calc["taxable_value"],
                    gst_rate=calc["gst_rate"],
                    cgst_amount=calc["cgst_amount"],
                    sgst_amount=calc["sgst_amount"],
                    igst_amount=calc["igst_amount"],
                    cess_amount=calc["cess_amount"],
                    item_total=calc["item_total"],
                )
            )

        grand_total_d = subtotal_d + cgst_total_d + sgst_total_d + igst_total_d + cess_total_d

        new_invoice = Invoice(
            invoice_number=payload.invoice_number,
            invoice_date=payload.invoice_date,
            supplier_gstin=payload.supplier_gstin,
            buyer_gstin=payload.buyer_gstin,
            place_of_supply=pos,
            status="FINALIZED",
            subtotal=float(quantize_currency(subtotal_d)),
            cgst_total=float(quantize_currency(cgst_total_d)),
            sgst_total=float(quantize_currency(sgst_total_d)),
            igst_total=float(quantize_currency(igst_total_d)),
            cess_total=float(quantize_currency(cess_total_d)),
            grand_total=float(quantize_currency(grand_total_d)),
            notes=payload.notes,
            items=db_items,
        )

        return repo.create(new_invoice)
