# main.py
from fastapi import FastAPI
from schemas import DetectResponse
from dispatcher import dispatch_alert
from logger import log_evidence, init_db, close_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.post("/process-alerts", response_model=DetectResponse)
async def process_alerts(response: DetectResponse):
    for alert in response.alerts:
        alert_dict = alert.dict()
        dispatch_alert(alert_dict)       # notify admins
        await log_evidence(alert_dict)   # log in DB
    return response
