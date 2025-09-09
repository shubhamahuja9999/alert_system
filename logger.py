# logger.py
from prisma import Prisma
from utils import generate_hash
from datetime import datetime

db = Prisma()

async def init_db():
    await db.connect()

async def close_db():
    await db.disconnect()

async def log_evidence(alert: dict):
    """
    Idempotent insert: skip if alert_id already exists.
    """
    existing = await db.anomalylog.find_first(
        where={"alert_id": alert.get("alert_id")}
    )
    if existing:
        return existing

    ts = alert.get("timestamp")
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            ts = datetime.utcnow()

    record_hash = generate_hash(alert)

    created = await db.anomalylog.create(
        data={
            "alert_id": alert.get("alert_id"),
            "tourist_id": alert.get("tourist_id"),
            "anomaly_type": alert.get("anomaly_type"),
            "alert_level": alert.get("alert_level"),
            "confidence_score": float(alert.get("confidence_score") or 0.0),
            "latitude": float(alert["location"]["lat"]),
            "longitude": float(alert["location"]["lng"]),
            "timestamp": ts,
            "raw_evidence": alert.get("raw_evidence") or {},
            "model_version": alert.get("model_version") or "",
            "hash": record_hash,
        }
    )
    return created


# helpers for admin queries
async def list_alerts(limit: int = 100, offset: int = 0):
    return await db.anomalylog.find_many(
        skip=offset, 
        take=limit, 
        order=[{"createdAt": "desc"}]
    )

async def get_alert_by_alert_id(alert_id: str):
    return await db.anomalylog.find_first(where={"alert_id": alert_id})
