"""
Development Seed Data Script (SAMPLE DATA ONLY)
Restores baseline statutory dataset and sample test cases.

GUARD: Loaded ONLY when APP_ENV or ENVIRONMENT is 'development'.
Production environments serve approved ingested rows only.
"""

import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

# Ensure apps/api/src is in pythonpath
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from smart_gst.audit.models import AuditLog
from smart_gst.auth.models import User
from smart_gst.common.security import get_password_hash
from smart_gst.config import settings
from smart_gst.db.base import Base
from smart_gst.db.session import SessionLocal, engine
from smart_gst.ingestion.models import NotificationDocument
from smart_gst.invoicing.models import Invoice, InvoiceItem
from smart_gst.rates.models import TariffHierarchy, TariffRateRule

# ENVIRONMENT GUARD
env = os.getenv("APP_ENV", os.getenv("ENVIRONMENT", settings.ENVIRONMENT)).lower()
if env != "development":
    print(f"FATAL: dev_seed.py can ONLY run in development environment! Detected: '{env}'")
    sys.exit(1)


# ==========================================
# 1. Authoritative CBIC Statutory Master Rates (SAMPLE DEV RECOVERY)
# ==========================================
SAMPLE_RATE_RULES: List[Dict[str, Any]] = [
    {
        "hsn_code": "42031010",
        "description": "Apparel and clothing accessories of leather or composition leather (Jackets, Coats)",
        "rate": 18.0,
        "schedule": "Schedule III",
        "serial_no": "111",
        "notification_no": "Notification No. 1/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "effective_from": "2017-07-01",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
        "verified_by": "CBIC Tariff Administration (SAMPLE)",
    },
    {
        "hsn_code": "85414011",
        "description": "Solar cells whether or not assembled in modules or made up into panels (Photovoltaic)",
        "rate": 12.0,
        "schedule": "Schedule II",
        "serial_no": "201A",
        "notification_no": "Notification No. 8/2021-Central Tax (Rate)",
        "notification_date": "2021-09-30",
        "effective_from": "2021-10-01",
        "effective_to": "2025-09-21",
        "source_url": "https://cbic-gst.gov.in/pdf/Notification8-CGST-Rate.pdf",
        "verified_by": "GST Council Secretariat (SAMPLE)",
    },
    {
        "hsn_code": "85414011",
        "description": "Solar cells whether or not assembled in modules or panels (Photovoltaic - GST Reform 2025)",
        "rate": 18.0,
        "schedule": "Schedule III",
        "serial_no": "185B",
        "notification_no": "Notification No. 15/2025-Central Tax (Rate)",
        "notification_date": "2025-09-18",
        "effective_from": "2025-09-22",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification15-2025-CGST-Rate.pdf",
        "verified_by": "GST Council Secretariat (SAMPLE)",
    },
    {
        "hsn_code": "09011110",
        "description": "Coffee beans, raw, unroasted, unbranded",
        "rate": 0.0,
        "schedule": "Schedule I",
        "serial_no": "45",
        "notification_no": "Notification No. 2/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "effective_from": "2017-07-01",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification2-CGST-Rate.pdf",
        "verified_by": "CBIC Tariff Administration (SAMPLE)",
    },
    {
        "hsn_code": "61091000",
        "description": "T-shirts, singlets and other vests of cotton, knitted or crocheted (Unit sale price <= Rs 1000)",
        "rate": 5.0,
        "schedule": "Schedule I",
        "serial_no": "180",
        "notification_no": "Notification No. 1/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "effective_from": "2017-07-01",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
        "verified_by": "CBIC Tariff Administration (SAMPLE)",
    },
    {
        "hsn_code": "61091000",
        "description": "T-shirts, singlets and other vests of cotton, knitted or crocheted (Unit sale price > Rs 1000)",
        "rate": 18.0,
        "schedule": "Schedule III",
        "serial_no": "154",
        "notification_no": "Notification No. 1/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "effective_from": "2017-07-01",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
        "verified_by": "CBIC Tariff Administration (SAMPLE)",
    },
    {
        "hsn_code": "99831300",
        "description": "Information technology (IT) software and cloud SaaS application subscription services",
        "rate": 18.0,
        "schedule": "Schedule III",
        "serial_no": "21",
        "notification_no": "Notification No. 11/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "effective_from": "2017-07-01",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification11-CGST-Rate.pdf",
        "verified_by": "CBIC Services Directorate (SAMPLE)",
    },
    {
        "hsn_code": "87032391",
        "description": "Motor cars and other motor vehicles (>1500cc luxury segment, engine capacity >1500cc)",
        "rate": 40.0,
        "schedule": "Schedule IV",
        "serial_no": "52",
        "notification_no": "Notification No. 1/2017-Central Tax (Rate)",
        "notification_date": "2017-06-28",
        "effective_from": "2017-07-01",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
        "verified_by": "CBIC Tariff Administration (SAMPLE)",
    },
    {
        "hsn_code": "30049011",
        "description": "Medicaments of Ayurvedic system of medicine manufactured in accordance with Ayurvedic Pharmacopoeia",
        "rate": 5.0,
        "schedule": "Schedule I",
        "serial_no": "63",
        "notification_no": "Notification No. 1/2018-Central Tax (Rate)",
        "notification_date": "2018-01-25",
        "effective_from": "2018-01-25",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification1-2018-CGST-Rate.pdf",
        "verified_by": "CBIC Pharma Cell (SAMPLE)",
    },
    {
        "hsn_code": "46021100",
        "description": "Basketwork, wickerwork and other articles of vegetable materials (Bamboo handicrafts)",
        "rate": 0.0,
        "schedule": "Schedule I",
        "serial_no": "198A",
        "notification_no": "Notification No. 27/2017-Central Tax (Rate)",
        "notification_date": "2017-09-22",
        "effective_from": "2017-09-22",
        "effective_to": None,
        "source_url": "https://cbic-gst.gov.in/pdf/Notification27-CGST-Rate.pdf",
        "verified_by": "Artisan Directorate (SAMPLE)",
    },
]


# ==========================================
# 2. CBIC Notifications Index
# ==========================================
SAMPLE_NOTIFICATIONS: List[Dict[str, Any]] = [
    {
        "notification_no": "Notification No. 1/2017-Central Tax (Rate)",
        "title": "Principal Rate Schedule for Goods under Central Goods and Services Tax Act, 2017",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
        "sha256_hash": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
        "page_count": 142,
        "status": "APPROVED",
        "supersedes": None,
    },
    {
        "notification_no": "Notification No. 2/2017-Central Tax (Rate)",
        "title": "Exempt Goods Schedule under Central Goods and Services Tax Act, 2017",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification2-CGST-Rate.pdf",
        "sha256_hash": "b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01",
        "page_count": 48,
        "status": "APPROVED",
        "supersedes": None,
    },
    {
        "notification_no": "Notification No. 11/2017-Central Tax (Rate)",
        "title": "Rate Schedule for Services under Central Goods and Services Tax Act, 2017",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification11-CGST-Rate.pdf",
        "sha256_hash": "c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef012",
        "page_count": 64,
        "status": "APPROVED",
        "supersedes": None,
    },
    {
        "notification_no": "Notification No. 27/2017-Central Tax (Rate)",
        "title": "Concessional GST Rate Schedule for Handicraft Goods & Artisan Wickerwork",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification27-CGST-Rate.pdf",
        "sha256_hash": "d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0123",
        "page_count": 12,
        "status": "APPROVED",
        "supersedes": "Notification No. 1/2017-Central Tax (Rate)",
    },
    {
        "notification_no": "Notification No. 1/2018-Central Tax (Rate)",
        "title": "Amendment to Rate Schedule for Pharmaceutical & Ayush Medicaments",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification1-2018-CGST-Rate.pdf",
        "sha256_hash": "e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01234",
        "page_count": 18,
        "status": "APPROVED",
        "supersedes": "Notification No. 1/2017-Central Tax (Rate)",
    },
    {
        "notification_no": "Notification No. 8/2021-Central Tax (Rate)",
        "title": "Rationalization of Rates on Renewable Energy Devices and Solar Inverters",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification8-CGST-Rate.pdf",
        "sha256_hash": "f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef012345",
        "page_count": 8,
        "status": "SUPERSEDED",
        "supersedes": "Notification No. 1/2017-Central Tax (Rate)",
    },
    {
        "notification_no": "Notification No. 15/2025-Central Tax (Rate)",
        "title": "GST Rate Structure Simplification 2025 (Transition to 4-tier 0/5/18/40 Schedule)",
        "category": "Central Tax",
        "url": "https://cbic-gst.gov.in/pdf/Notification15-2025-CGST-Rate.pdf",
        "sha256_hash": "0718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0123456",
        "page_count": 96,
        "status": "APPROVED",
        "supersedes": "Notification No. 8/2021-Central Tax (Rate)",
    },
]


# ==========================================
# 3. Tariff Hierarchy Trees
# ==========================================
SAMPLE_HIERARCHY: List[Dict[str, Any]] = [
    {
        "code": "42",
        "level": "chapter",
        "title": "Articles of leather; saddlery and harness; travel goods, handbags",
        "parent_id": None,
    },
    {
        "code": "4203",
        "level": "heading",
        "title": "Articles of apparel and clothing accessories, of leather or composition leather",
        "parent_id": "42",
    },
    {
        "code": "420310",
        "level": "sub_heading",
        "title": "Apparel (jackets, coats, trousers)",
        "parent_id": "4203",
    },
    {
        "code": "42031010",
        "level": "tariff_item",
        "title": "Jackets and coats of leather or composition leather",
        "parent_id": "420310",
    },
    {
        "code": "85",
        "level": "chapter",
        "title": "Electrical machinery and equipment and parts thereof",
        "parent_id": None,
    },
    {
        "code": "8541",
        "level": "heading",
        "title": "Diodes, transistors and similar semiconductor devices; photosensitive devices",
        "parent_id": "85",
    },
    {
        "code": "854140",
        "level": "sub_heading",
        "title": "Photosensitive semiconductor devices, including photovoltaic cells",
        "parent_id": "8541",
    },
    {
        "code": "85414011",
        "level": "tariff_item",
        "title": "Solar cells whether or not assembled in modules or panels",
        "parent_id": "854140",
    },
    {"code": "09", "level": "chapter", "title": "Coffee, tea, mate and spices", "parent_id": None},
    {
        "code": "0901",
        "level": "heading",
        "title": "Coffee, whether or not roasted or decaffeinated; coffee husks and skins",
        "parent_id": "09",
    },
    {
        "code": "090111",
        "level": "sub_heading",
        "title": "Coffee, not roasted: Not decaffeinated",
        "parent_id": "0901",
    },
    {
        "code": "09011110",
        "level": "tariff_item",
        "title": "Coffee beans, raw, unroasted, unbranded",
        "parent_id": "090111",
    },
    {
        "code": "61",
        "level": "chapter",
        "title": "Articles of apparel and clothing accessories, knitted or crocheted",
        "parent_id": None,
    },
    {
        "code": "6109",
        "level": "heading",
        "title": "T-shirts, singlets and other vests, knitted or crocheted",
        "parent_id": "61",
    },
    {"code": "610910", "level": "sub_heading", "title": "Of cotton", "parent_id": "6109"},
    {
        "code": "61091000",
        "level": "tariff_item",
        "title": "T-shirts, singlets and other vests of cotton, knitted or crocheted",
        "parent_id": "610910",
    },
    {
        "code": "99",
        "level": "chapter",
        "title": "Services Accounting Code (SAC Master Schedule)",
        "parent_id": None,
    },
    {
        "code": "9983",
        "level": "heading",
        "title": "Other professional, technical and business services",
        "parent_id": "99",
    },
    {
        "code": "998313",
        "level": "sub_heading",
        "title": "Information technology (IT) software and infrastructure services",
        "parent_id": "9983",
    },
    {
        "code": "99831300",
        "level": "tariff_item",
        "title": "IT software and cloud SaaS application subscription services",
        "parent_id": "998313",
    },
    {
        "code": "87",
        "level": "chapter",
        "title": "Vehicles other than railway or tramway rolling-stock",
        "parent_id": None,
    },
    {
        "code": "8703",
        "level": "heading",
        "title": "Motor cars and other motor vehicles principally designed for transport of persons",
        "parent_id": "87",
    },
    {
        "code": "870323",
        "level": "sub_heading",
        "title": "Of a cylinder capacity exceeding 1500 cc but not exceeding 3000 cc",
        "parent_id": "8703",
    },
    {
        "code": "87032391",
        "level": "tariff_item",
        "title": "Motor cars exceeding 1500cc luxury class",
        "parent_id": "870323",
    },
]


# ==========================================
# 4. Users
# ==========================================
SAMPLE_USERS: List[Dict[str, Any]] = [
    {"email": "admin@smartgst.in", "password": "AdminPass123!", "role": "ADMIN", "is_active": True},
    {
        "email": "accountant@smartgst.in",
        "password": "AccountantPass123!",
        "role": "ACCOUNTANT",
        "is_active": True,
    },
    {
        "email": "auditor@smartgst.in",
        "password": "AuditorPass123!",
        "role": "VIEWER",
        "is_active": True,
    },
]


# ==========================================
# 5. Rule 46 Compliant Invoices
# ==========================================
SAMPLE_INVOICES: List[Dict[str, Any]] = [
    {
        "invoice_number": "INV/2026-27/0001",
        "invoice_date": "2026-10-09",
        "supplier_gstin": "27AABCU9603R1ZN",
        "buyer_gstin": "29AABCU9603R1ZM",
        "place_of_supply": "29-Karnataka",
        "status": "FINALIZED",
        "subtotal": 125000.00,
        "cgst_total": 0.00,
        "sgst_total": 0.00,
        "igst_total": 22500.00,
        "cess_total": 0.00,
        "grand_total": 147500.00,
        "notes": "SAMPLE: Interstate Cloud Services B2B Invoice under IGST Act Section 7.",
        "items": [
            {
                "product_name": "Enterprise Cloud SaaS Subscription (1 Year)",
                "hsn_code": "99831300",
                "quantity": 1,
                "unit_price": 125000.00,
                "taxable_value": 125000.00,
                "gst_rate": 18.0,
                "cgst_amount": 0.00,
                "sgst_amount": 0.00,
                "igst_amount": 22500.00,
                "cess_amount": 0.00,
                "item_total": 147500.00,
            }
        ],
    },
    {
        "invoice_number": "INV/2026-27/0002",
        "invoice_date": "2026-10-08",
        "supplier_gstin": "27AABCU9603R1ZN",
        "buyer_gstin": "27XYZAB1234C1Z5",
        "place_of_supply": "27-Maharashtra",
        "status": "FINALIZED",
        "subtotal": 54000.00,
        "cgst_total": 4860.00,
        "sgst_total": 4860.00,
        "igst_total": 0.00,
        "cess_total": 0.00,
        "grand_total": 63720.00,
        "notes": "SAMPLE: Intrastate Leather Apparel Supply subject to CGST (9%) + SGST (9%).",
        "items": [
            {
                "product_name": "Men's Classic Leather Biker Jacket with Brass Zips",
                "hsn_code": "42031010",
                "quantity": 6,
                "unit_price": 9000.00,
                "taxable_value": 54000.00,
                "gst_rate": 18.0,
                "cgst_amount": 4860.00,
                "sgst_amount": 4860.00,
                "igst_amount": 0.00,
                "cess_amount": 0.00,
                "item_total": 63720.00,
            }
        ],
    },
]


# ==========================================
# 6. Audit Trail Logs
# ==========================================
SAMPLE_AUDIT_LOGS: List[Dict[str, Any]] = [
    {
        "action": "CLASSIFICATION_EVALUATED",
        "resource": "HSN_CLASSIFIER",
        "role": "ADMIN",
        "user_id": "admin@smartgst.in",
        "input_data": {"query": "leather jacket with zip", "mode": "INTRA_STATE"},
        "output_data": {"suggested_hsn": "42031010", "gst_rate": 18.0, "confidence": 93.3},
    },
    {
        "action": "INVOICE_FINALIZED",
        "resource": "INVOICE_ENGINE",
        "role": "ACCOUNTANT",
        "user_id": "accountant@smartgst.in",
        "input_data": {"invoice_number": "INV/2026-27/0001", "grand_total": 147500.00},
        "output_data": {"status": "LOCKED", "hash": "sha256-sample-audit-0001"},
    },
]


def run_seed():
    print(f"[*] Starting Smart GST Dev Seed (ENVIRONMENT={env})...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Clear existing rows to prevent duplicate primary key collisions in dev
        print(" -> Clearing dev tables...")
        db.query(InvoiceItem).delete()
        db.query(Invoice).delete()
        db.query(TariffRateRule).delete()
        db.query(TariffHierarchy).delete()
        db.query(NotificationDocument).delete()
        db.query(AuditLog).delete()
        db.query(User).delete()
        db.commit()

        # 1. Seed Rate Rules
        print(f" -> Seeding {len(SAMPLE_RATE_RULES)} tariff rate rules...")
        for r in SAMPLE_RATE_RULES:
            db.add(
                TariffRateRule(
                    id=str(uuid.uuid4()),
                    hsn_code=r["hsn_code"],
                    description=r["description"],
                    rate=r["rate"],
                    schedule=r["schedule"],
                    serial_no=r["serial_no"],
                    notification_no=r["notification_no"],
                    notification_date=r["notification_date"],
                    effective_from=r["effective_from"],
                    effective_to=r.get("effective_to"),
                    source_url=r["source_url"],
                    verified_by=r.get("verified_by", "SAMPLE DATA"),
                )
            )

        # 2. Seed Hierarchy
        print(f" -> Seeding {len(SAMPLE_HIERARCHY)} tariff hierarchy nodes...")
        for h in SAMPLE_HIERARCHY:
            db.add(
                TariffHierarchy(
                    code=h["code"], level=h["level"], title=h["title"], parent_id=h["parent_id"]
                )
            )

        # 3. Seed Notifications
        print(f" -> Seeding {len(SAMPLE_NOTIFICATIONS)} CBIC notifications...")
        for n in SAMPLE_NOTIFICATIONS:
            db.add(
                NotificationDocument(
                    notification_no=n["notification_no"],
                    title=n["title"],
                    category=n["category"],
                    url=n["url"],
                    sha256_hash=n["sha256_hash"],
                    page_count=n["page_count"],
                    status=n["status"],
                    supersedes=n.get("supersedes"),
                )
            )

        # 4. Seed Users
        print(f" -> Seeding {len(SAMPLE_USERS)} authentication users...")
        for u in SAMPLE_USERS:
            db.add(
                User(
                    email=str(u["email"]),
                    hashed_password=get_password_hash(str(u["password"])),
                    role=str(u["role"]),
                    is_active=bool(u["is_active"]),
                )
            )

        # 5. Seed Invoices
        print(f" -> Seeding {len(SAMPLE_INVOICES)} Rule 46 invoices...")
        for inv_data in SAMPLE_INVOICES:
            items_list: List[Dict[str, Any]] = list(inv_data.get("items", []))
            inv = Invoice(
                id=str(uuid.uuid4()),
                invoice_number=str(inv_data["invoice_number"]),
                invoice_date=str(inv_data["invoice_date"]),
                supplier_gstin=str(inv_data["supplier_gstin"]),
                buyer_gstin=str(inv_data["buyer_gstin"]),
                place_of_supply=str(inv_data["place_of_supply"]),
                status=str(inv_data["status"]),
                subtotal=float(inv_data["subtotal"]),
                cgst_total=float(inv_data["cgst_total"]),
                sgst_total=float(inv_data["sgst_total"]),
                igst_total=float(inv_data["igst_total"]),
                cess_total=float(inv_data["cess_total"]),
                grand_total=float(inv_data["grand_total"]),
                notes=str(inv_data["notes"]) if inv_data.get("notes") else None,
            )
            db.add(inv)
            db.flush()

            for it in items_list:
                item = InvoiceItem(
                    id=str(uuid.uuid4()),
                    invoice_id=inv.id,
                    product_name=str(it["product_name"]),
                    hsn_code=str(it["hsn_code"]),
                    quantity=int(it["quantity"]),
                    unit_price=float(it["unit_price"]),
                    taxable_value=float(it["taxable_value"]),
                    gst_rate=float(it["gst_rate"]),
                    cgst_amount=float(it["cgst_amount"]),
                    sgst_amount=float(it["sgst_amount"]),
                    igst_amount=float(it["igst_amount"]),
                    cess_amount=float(it["cess_amount"]),
                    item_total=float(it["item_total"]),
                )
                db.add(item)

        # 6. Seed Audit Logs
        print(f" -> Seeding {len(SAMPLE_AUDIT_LOGS)} initial audit logs...")
        for a in SAMPLE_AUDIT_LOGS:
            db.add(
                AuditLog(
                    id=str(uuid.uuid4()),
                    action=a["action"],
                    resource=a["resource"],
                    role=a["role"],
                    user_id=a["user_id"],
                    input_data=a["input_data"],
                    output_data=a["output_data"],
                    timestamp=datetime.now(timezone.utc),
                )
            )

        db.commit()
        print("[✓] Dev seed successfully applied!")
    except Exception as e:
        db.rollback()
        print(f"[x] Error applying dev seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
