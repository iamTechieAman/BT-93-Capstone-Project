"""
Unit Tests for Decimal Tax Domain Engine.
Validates:
1. Intra-state split: exact 50/50 division into CGST and SGST.
2. Inter-state IGST calculation without CGST/SGST.
3. Compensation Cess calculation.
4. Decimal rounding edge cases using ROUND_HALF_UP (fractional paise).
"""

import pytest

from smart_gst.invoicing.service import TaxDomainService

INTRA_STATE_CASES = [
    # (qty, unit_price, gst_rate, expected_taxable, expected_cgst, expected_sgst, expected_total)
    (1, 1000.0, 18.0, 1000.0, 90.0, 90.0, 1180.0),
    (2, 500.0, 12.0, 1000.0, 60.0, 60.0, 1120.0),
    (10, 100.0, 5.0, 1000.0, 25.0, 25.0, 1050.0),
    (1, 2500.0, 28.0, 2500.0, 350.0, 350.0, 3200.0),
]


@pytest.mark.parametrize(
    "qty,unit_price,gst_rate,exp_taxable,exp_cgst,exp_sgst,exp_total", INTRA_STATE_CASES
)
def test_intra_state_tax_calculation_cases(
    qty, unit_price, gst_rate, exp_taxable, exp_cgst, exp_sgst, exp_total
):
    res = TaxDomainService.calculate_line_item(
        quantity=qty, unit_price=unit_price, gst_rate=gst_rate, is_interstate=False
    )
    assert res["taxable_value"] == exp_taxable
    assert res["cgst_amount"] == exp_cgst
    assert res["sgst_amount"] == exp_sgst
    assert res["igst_amount"] == 0.0
    assert res["item_total"] == exp_total


INTER_STATE_CASES = [
    # (qty, unit_price, gst_rate, expected_taxable, expected_igst, expected_total)
    (1, 1000.0, 18.0, 1000.0, 180.0, 1180.0),
    (2, 500.0, 12.0, 1000.0, 120.0, 1120.0),
    (1, 10000.0, 28.0, 10000.0, 2800.0, 12800.0),
]


@pytest.mark.parametrize(
    "qty,unit_price,gst_rate,exp_taxable,exp_igst,exp_total", INTER_STATE_CASES
)
def test_inter_state_tax_calculation_cases(
    qty, unit_price, gst_rate, exp_taxable, exp_igst, exp_total
):
    res = TaxDomainService.calculate_line_item(
        quantity=qty, unit_price=unit_price, gst_rate=gst_rate, is_interstate=True
    )
    assert res["taxable_value"] == exp_taxable
    assert res["cgst_amount"] == 0.0
    assert res["sgst_amount"] == 0.0
    assert res["igst_amount"] == exp_igst
    assert res["item_total"] == exp_total


CESS_CALCULATION_CASES = [
    # (qty, unit_price, gst_rate, cess_rate, exp_taxable, exp_igst, exp_cess, exp_total)
    (1, 100000.0, 28.0, 15.0, 100000.0, 28000.0, 15000.0, 143000.0),
    (2, 50000.0, 28.0, 12.0, 100000.0, 28000.0, 12000.0, 140000.0),
]


@pytest.mark.parametrize(
    "qty,unit_price,gst_rate,cess_rate,exp_taxable,exp_igst,exp_cess,exp_total",
    CESS_CALCULATION_CASES,
)
def test_compensation_cess_calculation_cases(
    qty, unit_price, gst_rate, cess_rate, exp_taxable, exp_igst, exp_cess, exp_total
):
    res = TaxDomainService.calculate_line_item(
        quantity=qty,
        unit_price=unit_price,
        gst_rate=gst_rate,
        is_interstate=True,
        cess_rate=cess_rate,
    )
    assert res["taxable_value"] == exp_taxable
    assert res["igst_amount"] == exp_igst
    assert res["cess_amount"] == exp_cess
    assert res["item_total"] == exp_total


ROUNDING_EDGE_CASES = [
    # (unit_price, gst_rate, is_interstate, exp_taxable, exp_cgst, exp_sgst, exp_igst, exp_total)
    # 333.33 @ 5% intra -> 16.6665 tax -> CGST 8.33, SGST 8.33 -> Total 349.99
    (333.33, 5.0, False, 333.33, 8.33, 8.33, 0.0, 349.99),
    # 99.99 @ 18% inter -> 17.9982 tax -> IGST 18.00 -> Total 117.99
    (99.99, 18.0, True, 99.99, 0.0, 0.0, 18.00, 117.99),
    # 1.05 @ 12% intra -> 0.126 tax -> CGST 0.06, SGST 0.06 -> Total 1.17
    (1.05, 12.0, False, 1.05, 0.06, 0.06, 0.0, 1.17),
]


@pytest.mark.parametrize(
    "unit_price,gst_rate,is_interstate,exp_taxable,exp_cgst,exp_sgst,exp_igst,exp_total",
    ROUNDING_EDGE_CASES,
)
def test_decimal_rounding_half_up_edge_cases(
    unit_price, gst_rate, is_interstate, exp_taxable, exp_cgst, exp_sgst, exp_igst, exp_total
):
    res = TaxDomainService.calculate_line_item(
        quantity=1, unit_price=unit_price, gst_rate=gst_rate, is_interstate=is_interstate
    )
    assert res["taxable_value"] == exp_taxable
    assert res["cgst_amount"] == exp_cgst
    assert res["sgst_amount"] == exp_sgst
    assert res["igst_amount"] == exp_igst
    assert res["item_total"] == exp_total


def test_invoice_creation_and_duplicate_validation(db_session):
    from smart_gst.common.errors import ValidationException
    from smart_gst.invoicing.repository import InvoiceRepository
    from smart_gst.invoicing.schemas import InvoiceCreatePayload, InvoiceLineItemInput

    repo = InvoiceRepository(db_session)
    payload = InvoiceCreatePayload(
        invoice_number="INV-DUP-01",
        invoice_date="2026-10-09",
        supplier_gstin="27AAPFU0939F1ZV",
        buyer_gstin="27AAPFU0939F1ZV",
        line_items=[
            InvoiceLineItemInput(
                product_name="Sample Item",
                hsn_code="42031010",
                quantity=1,
                unit_price=100.0,
                gst_rate=18.0,
            )
        ],
    )

    inv = TaxDomainService.create_invoice(repo, payload)
    assert inv.id is not None
    assert inv.invoice_number == "INV-DUP-01"

    # Duplicate should raise ValidationException
    with pytest.raises(ValidationException):
        TaxDomainService.create_invoice(repo, payload)

    # Repository queries
    assert repo.get_by_id(str(inv.id)) is not None
    assert repo.get_by_number("INV-DUP-01") is not None
    assert repo.get_by_id("non-existent") is None
    all_invs, count = repo.list_invoices(offset=0, limit=10)
    assert count >= 1
