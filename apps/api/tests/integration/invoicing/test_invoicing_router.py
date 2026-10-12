"""
Integration tests for Invoicing API endpoints (/api/v1/invoices/*).
"""


def test_invoice_create_and_fetch_workflow(client, auth_headers):
    payload = {
        "invoice_number": "INV-TEST-9001",
        "invoice_date": "2026-10-09",
        "supplier_gstin": "27AAPFU0939F1ZV",
        "buyer_gstin": "29ABCDE1234F1ZW",
        "place_of_supply": "29-Karnataka",
        "line_items": [
            {
                "product_name": "Men's Leather Jacket",
                "hsn_code": "42031010",
                "quantity": 2,
                "unit_price": 5000.0,
                "gst_rate": 18.0,
                "cess_rate": 0.0,
            }
        ],
    }

    create_res = client.post("/api/v1/invoices", json=payload, headers=auth_headers)
    assert create_res.status_code == 200
    inv = create_res.json()
    assert inv["invoice_number"] == "INV-TEST-9001"
    assert inv["subtotal"] == 10000.0
    assert inv["igst_total"] == 1800.0
    assert inv["grand_total"] == 11800.0
    assert inv["status"] == "FINALIZED"

    # Fetch by ID
    get_res = client.get(f"/api/v1/invoices/{inv['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == inv["id"]

    # List all invoices
    list_res = client.get("/api/v1/invoices")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
