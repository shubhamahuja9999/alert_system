# schemas.py
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime
import uuid

class Alert(BaseModel):
    alert_id: str = str(uuid.uuid4())
    tourist_id: str
    anomaly_type: str
    alert_level: str
    confidence_score: float
    location: Dict[str, float]
    timestamp: datetime
    model_version: str
    raw_evidence: Dict

class DetectResponse(BaseModel):
    status: str
    anomaly_count: int
    alerts: List[Alert]
