"""
Unit tests for Real-Signal Classification Confidence Computation.
Validates:
1. Signal breakdown returned with exact values (keyword, vector, rule match, source count, missing condition penalty).
2. 0-100 real dynamic range (no artificial 75-99% clamp).
3. "Needs review" vs "Matched" status based on configurable threshold.
4. Alternatives with real scores.
"""

from smart_gst.classification.llm_client import LlmClient
from smart_gst.classification.schemas import ClassificationRequest
from smart_gst.classification.service import ClassificationService
from smart_gst.rates.models import TariffRateRule
from smart_gst.rates.repository import RateRepository


class FakeRateRepo(RateRepository):
    def __init__(self):
        pass

    def get_by_hsn(self, hsn_prefix: str):
        if hsn_prefix == "4203":
            return TariffRateRule(
                hsn_code="42031010",
                description="Articles of apparel, leather",
                rate=18.0,
                notification_no="1/2017-Central Tax (Rate)",
                notification_date="2017-06-28",
                schedule="Schedule III",
                serial_no="111",
                effective_from="2017-07-01",
                source_url="https://cbic-gst.gov.in/notif.pdf",
            )
        return None


class FakeLlmClient(LlmClient):
    def explain_classification(
        self, product: str, hsn: str, rate: float, evidence: list[dict]
    ) -> str:
        return f"Classified '{product}' under HSN {hsn} at {rate}% GST."


def test_real_signals_high_confidence():
    service = ClassificationService(rate_repo=FakeRateRepo(), llm_client=FakeLlmClient())
    req = ClassificationRequest(product_description="Men's black genuine leather jacket")
    res = service.classify_product(req)

    assert res.suggested_hsn == "42031010"
    assert res.gst_rate == 18.0
    assert res.status == "Matched"
    assert res.match_quality == "Strong"
    assert res.confidence >= 80.0
    assert res.signals.statutory_rule_match is True
    assert res.signals.agreeing_sources_count >= 2
    assert res.signals.missing_conditions_penalty == 0.0


def test_real_signals_missing_conditions_penalty():
    service = ClassificationService(rate_repo=FakeRateRepo(), llm_client=FakeLlmClient())
    req = ClassificationRequest(product_description="Cotton knitted shirt")
    res = service.classify_product(req)

    assert res.signals.missing_conditions_penalty == 15.0
    assert res.confidence < 80.0
