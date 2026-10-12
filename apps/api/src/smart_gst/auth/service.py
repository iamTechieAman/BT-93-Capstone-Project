"""
Authentication Domain Service.
"""

from typing import Tuple

from smart_gst.auth.models import User
from smart_gst.auth.repository import UserRepository
from smart_gst.auth.schemas import LoginRequest, UserCreate
from smart_gst.common.errors import UnauthorizedException, ValidationException
from smart_gst.common.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, payload: LoginRequest) -> Tuple[User, str, str]:
        user = self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")
        if not user.is_active:
            raise UnauthorizedException("User account is inactive.")

        access_token = create_access_token(user_id=user.id, email=user.email, role=user.role)
        refresh_token = create_refresh_token(user_id=user.id, email=user.email)
        return user, access_token, refresh_token

    def register_user(self, payload: UserCreate) -> User:
        existing = self.user_repo.get_by_email(payload.email)
        if existing:
            raise ValidationException(
                f"User with email {payload.email} already exists.", code="USER_EXISTS"
            )

        new_user = User(
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            role=payload.role,
        )
        return self.user_repo.create(new_user)
