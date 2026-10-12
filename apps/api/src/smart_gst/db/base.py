"""
SQLAlchemy Declarative Base Metadata.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base model providing shared timestamp columns."""

    pass
