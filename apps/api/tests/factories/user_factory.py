import uuid

from smart_gst.auth.models import User
from smart_gst.common.security import get_password_hash


class UserFactory:
    @staticmethod
    def build(
        email: str = "testuser@smartgst.in",
        role: str = "VIEWER",
        password: str = "SecretPassword123!",
    ) -> User:
        return User(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=get_password_hash(password),
            role=role.upper(),
            is_active=True,
        )

    @staticmethod
    def create(
        db,
        email: str = "testuser@smartgst.in",
        role: str = "VIEWER",
        password: str = "SecretPassword123!",
    ) -> User:
        user = UserFactory.build(email=email, role=role, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
