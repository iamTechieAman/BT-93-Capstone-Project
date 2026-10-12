"""
Unit tests for Standardized Error Envelopes and Exceptions.
Format: {"code": str, "message": str, "request_id": str}
"""

from smart_gst.common.errors import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)


def test_app_exception_properties():
    exc = NotFoundException("HSN code not found")
    assert exc.code == "NOT_FOUND"
    assert exc.message == "HSN code not found"
    assert exc.status_code == 404

    val_exc = ValidationException("Missing invoice line items")
    assert val_exc.code == "VALIDATION_FAILED"
    assert val_exc.status_code == 400

    unauth_exc = UnauthorizedException("Session invalid")
    assert unauth_exc.code == "UNAUTHORIZED"
    assert unauth_exc.status_code == 401

    forbid_exc = ForbiddenException("Role not authorized")
    assert forbid_exc.code == "FORBIDDEN"
    assert forbid_exc.status_code == 403
