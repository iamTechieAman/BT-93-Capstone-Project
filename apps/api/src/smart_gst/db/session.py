"""
SQLAlchemy Engine and Session Management with PostgreSQL and SQLite support.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from smart_gst.common.logging import logger
from smart_gst.config import settings

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
except Exception as e:
    logger.warning(
        f"Database connection error with {settings.DATABASE_URL}: {e}. Falling back to SQLite."
    )
    engine = create_engine(
        "sqlite:///./smart_gst.db", connect_args={"check_same_thread": False}, pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency for database session life-cycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
