# schemas.py
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class Location(BaseModel):
    lat: float
    lng: float

class Alert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tourist_id: str
    anomaly_type: str
    alert_level: str
    confidence_score: float
    location: Location
    timestamp: datetime
    model_version: Optional[str] = None
    raw_evidence: Optional[Dict] = {}

    @validator("alert_level")
    def level_upper(cls, v):
        return v.upper()

class DetectResponse(BaseModel):
    status: str
    anomaly_count: int
    alerts: List[Alert]
