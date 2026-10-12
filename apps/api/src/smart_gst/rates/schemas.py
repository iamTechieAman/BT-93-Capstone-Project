from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class RateRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hsn_code: str
    description: str
    rate: float
    schedule: str
    serial_no: str
    notification_no: str
    notification_date: str
    effective_from: str
    effective_to: Optional[str] = None
    source_url: str


class HierarchyNodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    level: str
    title: str
    description: Optional[str] = None
    parent_id: Optional[str] = None
    conditions: Optional[List[Dict[str, Any]]] = None
    evaluation_factors: Optional[List[str]] = None
