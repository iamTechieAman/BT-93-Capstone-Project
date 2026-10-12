"""
Golden Dataset Verification Tests for CA-Confirmed Product Classifications.
Includes statutory rate resolution transitions before and after 22 Sep 2025
(Notification No. 09/2025 & 10/2025 Central Tax Rate changes).
"""

import pytest

from smart_gst.classification.schemas import ClassificationRequest
from smart_gst.classification.service import ClassificationService
from smart_gst.rates.models import TariffRateRule


class MockRateRepo:
    def __init__(self):
        self.rules = {
            "4203": TariffRateRule(
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
            "8541": TariffRateRule(
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
            "0901": TariffRateRule(
                hsn_code="09011110",
                description="Raw unroasted coffee beans",
                rate=0.0,
                notification_no="2/2017-Central Tax (Rate)",
                notification_date="2017-06-28",
                schedule="Schedule I",
                serial_no="45",
                effective_from="2017-07-01",
                source_url="https://cbic-gst.gov.in/pdf/Notification2-CGST-Rate.pdf",
            ),
            "9983": TariffRateRule(
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
            "8703": TariffRateRule(
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
        }

    def get_by_hsn(self, prefix: str):
        return self.rules.get(prefix)


class MockLlmClient:
    def explain_classification(self, product, hsn, rate, evidence):
        return f"Statutory classification for '{product}' mapped to HSN {hsn} at {rate}% GST."


CA_CONFIRMED_GOLDEN_CASES = [
    # (Product Description, Expected HSN, Expected GST Rate, Match Quality)
    ("Men's black genuine leather jacket with brass zippers", "42031010", 18.0, "Strong"),
    ("Photovoltaic solar cell panel 300W module", "85414011", 12.0, "Strong"),
    ("Raw unroasted organic Arabica coffee beans", "09011110", 0.0, "Strong"),
    ("Cloud SaaS enterprise accounting software subscription", "99831300", 18.0, "Strong"),
    (
        "Motor vehicle passenger car with spark-ignition exceeding 1500cc",
        "87032391",
        28.0,
        "Strong",
    ),
]


@pytest.mark.parametrize(
    "product_desc,expected_hsn,expected_rate,expected_quality", CA_CONFIRMED_GOLDEN_CASES
)
def test_ca_golden_dataset_classification_accuracy(
    product_desc, expected_hsn, expected_rate, expected_quality
):
    service = ClassificationService(rate_repo=MockRateRepo(), llm_client=MockLlmClient())
    req = ClassificationRequest(product_description=product_desc, invoice_date="2026-10-09")
    result = service.classify_product(req)

    assert result.suggested_hsn == expected_hsn
    assert result.gst_rate == expected_rate
    assert result.match_quality == expected_quality
    assert result.confidence >= 75.0
    assert result.status == "Matched"


DATE_TRANSITION_CASES = [
    # (Product, Invoice Date, Expected Rate Note / Effective text)
    ("Men's leather jacket", "2025-08-15", "18.0% as on 2025-08-15"),
    ("Men's leather jacket", "2025-09-22", "18.0% as on 2025-09-22"),
    ("Men's leather jacket", "2026-03-31", "18.0% as on 2026-03-31"),
]


@pytest.mark.parametrize("product_desc,invoice_date,expected_text", DATE_TRANSITION_CASES)
def test_ca_rate_resolution_date_transitions(product_desc, invoice_date, expected_text):
    service = ClassificationService(rate_repo=MockRateRepo(), llm_client=MockLlmClient())
    req = ClassificationRequest(product_description=product_desc, invoice_date=invoice_date)
    result = service.classify_product(req)
    assert result.effective_rate_text == expected_text
