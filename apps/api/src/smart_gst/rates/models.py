"""
Tariff Rate Rules and Relational Tariff Hierarchy Database Models.
"""

from sqlalchemy import JSON, Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from smart_gst.db.base import Base


class TariffHierarchy(Base):
    """
    Relational Tariff Hierarchy replacing standalone graph triples.
    chapter -> heading -> sub-heading -> tariff item with self-referencing parent_id.
    """

    __tablename__ = "tariff_hierarchy"

    code = Column(String(10), primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # CHAPTER, HEADING, SUBHEADING, TARIFF_ITEM
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(String(10), ForeignKey("tariff_hierarchy.code"), nullable=True, index=True)
    conditions = Column(JSON, nullable=True)
    evaluation_factors = Column(JSON, nullable=True)

    parent = relationship("TariffHierarchy", remote_side=[code], backref="children")


class TariffRateRule(Base):
    __tablename__ = "tariff_rate_rules"

    id = Column(String(50), primary_key=True, index=True)
    hsn_code = Column(String(10), nullable=False, index=True)
    description = Column(Text, nullable=False)
    rate = Column(Float, nullable=False)
    schedule = Column(String(50), nullable=False)
    serial_no = Column(String(50), nullable=False)
    notification_no = Column(String(100), nullable=False)
    notification_date = Column(String(50), nullable=False)
    effective_from = Column(String(50), nullable=False)
    effective_to = Column(String(50), nullable=True)
    source_url = Column(String(500), nullable=False)
    verified_by = Column(String(100), nullable=True)
