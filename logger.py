# logger.py
from prisma import Prisma
from utils import generate_hash

db = Prisma()

async def init_db():
    await db.connect()

async def close_db():
    await db.disconnect()

async def log_evidence(alert: dict):
    record_hash = generate_hash(alert)
    await db.anomalylog.create(
        data={
            "tourist_id": alert["tourist_id"],
            "anomaly_type": alert["anomaly_type"],
            "alert_level": alert["alert_level"],
            "confidence_score": alert["confidence_score"],
            "latitude": alert["location"]["lat"],
            "longitude": alert["location"]["lng"],
            "timestamp": alert["timestamp"],
            "raw_evidence": alert["raw_evidence"],
            "model_version": alert["model_version"],
            "hash": record_hash
        }
    )
