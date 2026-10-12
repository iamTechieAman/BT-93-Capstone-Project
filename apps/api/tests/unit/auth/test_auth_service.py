"""
Unit tests for Auth Domain Service and Security Primitives.
Uses pytest.mark.parametrize for credential testing and claim verification.
"""

from datetime import timedelta

import pytest

from smart_gst.common.errors import UnauthorizedException
from smart_gst.common.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)

PASSWORD_TEST_VECTORS = [
    ("SuperSecret123!", True),
    ("AnotherP@ssw0rd#2026", True),
    ("Short", True),
    ("Special!@#$%^&*()_+{}[]:;<>?,./", True),
]


@pytest.mark.parametrize("raw_password,is_valid_attempt", PASSWORD_TEST_VECTORS)
def test_password_hashing_and_verification_matrix(raw_password, is_valid_attempt):
    hashed = get_password_hash(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is is_valid_attempt
    assert verify_password("InvalidAttempt!", hashed) is False


TOKEN_ROLE_VECTORS = [
    ("usr_001", "admin@smartgst.in", "ADMIN"),
    ("usr_002", "auditor@smartgst.in", "AUDITOR"),
    ("usr_003", "viewer@smartgst.in", "VIEWER"),
]


@pytest.mark.parametrize("user_id,email,role", TOKEN_ROLE_VECTORS)
def test_jwt_access_token_role_claims(user_id, email, role):
    access_tok = create_access_token(user_id=user_id, email=email, role=role)
    payload = decode_token(access_tok)

    assert payload["sub"] == user_id
    assert payload["email"] == email
    assert payload["role"] == role
    assert payload["type"] == "access"


def test_expired_token_handling():
    expired_tok = create_access_token(
        user_id="usr_exp", email="expired@smartgst.in", expires_delta=timedelta(seconds=-10)
    )
    with pytest.raises(UnauthorizedException) as exc_info:
        decode_token(expired_tok)
    assert "expired" in exc_info.value.message.lower()
