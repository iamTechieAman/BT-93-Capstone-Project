"""
Unified API Error Handling and Standardized JSON Error Response Format.
Format: {"code": str, "message": str, "request_id": str}
"""

from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None


class AppException(HTTPException):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[dict] = None,
    ):
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.code = code
        self.message = message


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(code="NOT_FOUND", message=message, status_code=status.HTTP_404_NOT_FOUND)


class ValidationException(AppException):
    def __init__(self, message: str, code: str = "VALIDATION_FAILED"):
        super().__init__(code=code, message=message, status_code=status.HTTP_400_BAD_REQUEST)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(code="FORBIDDEN", message=message, status_code=status.HTTP_403_FORBIDDEN)


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "req-unknown")
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code, "message": exc.message, "request_id": request_id},
            headers=exc.headers,
        )
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "request_id": request_id,
        },
    )


async def generic_http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "req-unknown")
    if isinstance(exc, HTTPException):
        code = "HTTP_ERROR"
        if exc.status_code == 404:
            code = "NOT_FOUND"
        elif exc.status_code == 401:
            code = "UNAUTHORIZED"
        elif exc.status_code == 403:
            code = "FORBIDDEN"
        elif exc.status_code == 422:
            code = "UNPROCESSABLE_ENTITY"
        elif exc.status_code == 400:
            code = "BAD_REQUEST"

        message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": code, "message": message, "request_id": request_id},
            headers=exc.headers,
        )
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "request_id": request_id,
        },
    )
