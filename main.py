# main.py
from fastapi import FastAPI, BackgroundTasks, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemas import DetectResponse
from dispatcher import dispatch_alert_background
from logger import init_db, close_db, log_evidence, list_alerts, get_alert_by_alert_id
from utils import append_detection_log
from typing import Any
from datetime import datetime
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(title="Alert System", lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    response = FileResponse("static/index.html")
    # Add CSP headers to allow inline scripts and styles
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

@app.get("/api")
def api_info():
    return {
        "message": "Alert System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "process_alerts": "/process-alerts",
            "get_alerts": "/alerts",
            "get_alert": "/alerts/{alert_id}",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}

@app.post("/process-alerts", response_model=DetectResponse)
async def process_alerts(response: DetectResponse, bg: BackgroundTasks):
    """
    Accepts the model's DetectResponse JSON and:
      - appends to local logs/detections.log
      - persists each alert to Postgres (Prisma)
      - dispatches notifications in background
    """
    # append whole DetectResponse to local log (for audit)
    append_detection_log(response.dict())

    for alert in response.alerts:
        alert_dict = alert.dict()
        # persist to DB (idempotent)
        await log_evidence(alert_dict)
        # background dispatch (email/sms/webhook)
        bg.add_task(dispatch_alert_background, alert_dict)

    return response

# Admin query endpoints
@app.get("/alerts")
async def get_alerts(limit: int = 100, offset: int = 0):
    rows = await list_alerts(limit=limit, offset=offset)
    return rows

@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    row = await get_alert_by_alert_id(alert_id)
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")
    return row
