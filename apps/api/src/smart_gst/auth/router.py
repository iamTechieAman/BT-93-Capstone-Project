"""
Authentication API Router under /api/v1/auth.
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from smart_gst.auth.repository import UserRepository
from smart_gst.auth.schemas import LoginRequest, TokenResponse, UserResponse
from smart_gst.auth.service import AuthService
from smart_gst.common.security import clear_auth_cookies, get_current_user_payload, set_auth_cookies
from smart_gst.db.session import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    user, access_token, refresh_token = auth_service.authenticate_user(payload)

    # Set httpOnly cookies for security
    set_auth_cookies(response, access_token, refresh_token)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_payload: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_payload["sub"])
    if not user:
        return UserResponse(
            id=user_payload.get("sub", "guest"),
            email=user_payload.get("email", "guest@smartgst.in"),
            role=user_payload.get("role", "VIEWER"),
            is_active=True,
        )
    return UserResponse.model_validate(user)


@router.post("/logout")
def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Successfully logged out."}
