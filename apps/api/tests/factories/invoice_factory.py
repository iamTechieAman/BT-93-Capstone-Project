import uuid

from smart_gst.invoicing.models import Invoice, InvoiceItem
from smart_gst.invoicing.service import TaxDomainService


class InvoiceFactory:
    @staticmethod
    def build(
        invoice_number: str = "INV-2026-0001",
        supplier_gstin: str = "27AAPFU0939F1ZV",
        buyer_gstin: str = "29ABCDE1234F1ZW",
        place_of_supply: str = "29-Karnataka",
        status: str = "DRAFT",
        items_data: list[dict] = None,
    ) -> Invoice:
        if items_data is None:
            items_data = [
                {
                    "product_name": "Leather Jacket",
                    "hsn_code": "42031010",
                    "quantity": 1,
                    "unit_price": 5000.0,
                    "gst_rate": 18.0,
                    "cess_rate": 0.0,
                }
            ]

        is_interstate = supplier_gstin[:2] != buyer_gstin[:2]
        invoice_id = str(uuid.uuid4())

        subtotal = 0.0
        cgst_total = 0.0
        sgst_total = 0.0
        igst_total = 0.0
        cess_total = 0.0
        grand_total = 0.0

        invoice_items = []
        for it in items_data:
            calc = TaxDomainService.calculate_line_item(
                quantity=it["quantity"],
                unit_price=it["unit_price"],
                gst_rate=it["gst_rate"],
                is_interstate=is_interstate,
                cess_rate=it.get("cess_rate", 0.0),
            )

            item = InvoiceItem(
                id=str(uuid.uuid4()),
                invoice_id=invoice_id,
                product_name=it["product_name"],
                hsn_code=it["hsn_code"],
                quantity=it["quantity"],
                unit_price=it["unit_price"],
                taxable_value=calc["taxable_value"],
                gst_rate=it["gst_rate"],
                cgst_amount=calc["cgst_amount"],
                sgst_amount=calc["sgst_amount"],
                igst_amount=calc["igst_amount"],
                cess_amount=calc["cess_amount"],
                item_total=calc["item_total"],
            )
            invoice_items.append(item)

            subtotal += calc["taxable_value"]
            cgst_total += calc["cgst_amount"]
            sgst_total += calc["sgst_amount"]
            igst_total += calc["igst_amount"]
            cess_total += calc["cess_amount"]
            grand_total += calc["item_total"]

        invoice = Invoice(
            id=invoice_id,
            invoice_number=invoice_number,
            invoice_date="2026-10-09",
            supplier_gstin=supplier_gstin,
            buyer_gstin=buyer_gstin,
            place_of_supply=place_of_supply,
            status=status,
            subtotal=round(subtotal, 2),
            cgst_total=round(cgst_total, 2),
            sgst_total=round(sgst_total, 2),
            igst_total=round(igst_total, 2),
            cess_total=round(cess_total, 2),
            grand_total=round(grand_total, 2),
            items=invoice_items,
        )
        return invoice

    @staticmethod
    def create(db, **kwargs) -> Invoice:
        inv = InvoiceFactory.build(**kwargs)
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return inv
