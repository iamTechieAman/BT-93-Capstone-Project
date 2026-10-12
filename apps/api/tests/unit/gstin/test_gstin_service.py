"""
Unit tests for GSTIN Statutory Validator Service & Mod-36 Checksum Engine.
Uses pytest.mark.parametrize across the full matrix of valid and invalid GSTIN vectors.
"""

import pytest

from smart_gst.gstin.service import GstinService, calculate_mod36_checksum

VALID_GSTIN_VECTORS = [
    # (GSTIN, State Code, State Name, PAN, Expected Checksum)
    ("27AAPFU0939F1ZV", "27", "Maharashtra", "AAPFU0939F", "V"),
    ("29ABCDE1234F1ZW", "29", "Karnataka", "ABCDE1234F", "W"),
    ("07AAAAA0000A1Z4", "07", "Delhi", "AAAAA0000A", "4"),
    ("33AAAAA0000A1Z9", "33", "Tamil Nadu", "AAAAA0000A", "9"),
    ("24AAAAA0000A1Z8", "24", "Gujarat", "AAAAA0000A", "8"),
    ("06AAAAA0000A1Z6", "06", "Haryana", "AAAAA0000A", "6"),
    ("97AAAAA0000A1ZV", "97", "Other Territory", "AAAAA0000A", "V"),
]


@pytest.mark.parametrize("gstin,state_code,state_name,pan,expected_checksum", VALID_GSTIN_VECTORS)
def test_valid_gstin_verification_matrix(gstin, state_code, state_name, pan, expected_checksum):
    service = GstinService()
    res = service.verify_gstin(gstin)

    assert res.format_valid is True
    assert res.checksum_valid is True
    assert res.verification_status == "PASSED"
    assert res.state_code == state_code
    assert res.state_name == state_name
    assert res.pan == pan
    assert res.headline == "Format valid. Registration not verified."
    assert res.registration_verified is False


INVALID_GSTIN_VECTORS = [
    # (GSTIN, Expected Failure Snippet)
    ("27AAPFU0939F1Z", "Length must be exactly 15"),
    ("27AAPFU0939F1ZEXTRA", "Length must be exactly 15"),
    ("99AAPFU0939F1ZV", "Invalid state code"),
    ("271234U0939F1ZV", "Invalid PAN structure"),
    ("27AAPFU0939F1AV", "14th character must be 'Z'"),
    ("27AAPFU0939F1ZX", "Modulus-36 checksum mismatch"),
    ("29ABCDE1234F1ZX", "Modulus-36 checksum mismatch"),
]


@pytest.mark.parametrize("gstin,failure_snippet", INVALID_GSTIN_VECTORS)
def test_invalid_gstin_verification_matrix(gstin, failure_snippet):
    service = GstinService()
    res = service.verify_gstin(gstin)

    assert res.format_valid is False
    assert res.verification_status == "FAILED"
    assert res.headline == "Format invalid."
    assert any(failure_snippet.lower() in f.lower() for f in res.validation_failures) or any(
        failure_snippet.lower() in w.lower() for w in res.warnings
    )


def test_mod36_checksum_exact():
    assert calculate_mod36_checksum("27AAPFU0939F1Z") == "V"
    assert calculate_mod36_checksum("29ABCDE1234F1Z") == "W"
    assert calculate_mod36_checksum("07AAAAA0000A1Z") == "4"


def test_gstin_invalid_entity_digit():
    service = GstinService()
    res = service.verify_gstin("27AAPFU0939F0ZV")  # '0' is invalid entity
    assert res.format_valid is False
    assert res.verification_status == "FAILED"


def test_gstin_live_provider_mode(monkeypatch):
    from smart_gst.config import settings

    monkeypatch.setattr(settings, "GST_PROVIDER_API_KEY", "test-gsp-key")
    monkeypatch.setattr(settings, "GST_PROVIDER_NAME", "Licensed GSP Mock")

    service = GstinService()
    res = service.verify_gstin("27AAPFU0939F1ZV")
    assert res.format_valid is True
    assert res.registration_verified is True
    assert res.taxpayer_status == "Active"
    assert res.provider_name == "Licensed GSP Mock"


def test_gstin_caching_behavior(db_session):
    from smart_gst.gstin.repository import GstinCacheRepository

    cache_repo = GstinCacheRepository(db_session)
    service = GstinService(cache_repo=cache_repo)

    # First lookup -> populates cache
    res1 = service.verify_gstin("27AAPFU0939F1ZV")
    assert res1.cached is False

    # Second lookup -> returns from cache
    res2 = service.verify_gstin("27AAPFU0939F1ZV")
    assert res2.cached is True
    assert res2.state_name == "Maharashtra"
