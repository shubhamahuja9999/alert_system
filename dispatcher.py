# dispatcher.py
import asyncio
import logging
import httpx
from config import ADMIN_EMAILS, ADMIN_PHONE, SEVERITY_ACTIONS, WEBHOOK_URL, EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_FROM, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM

logger = logging.getLogger("dispatcher")
logger.setLevel(logging.INFO)

async def _post_webhook(alerts: list):
    if not WEBHOOK_URL:
        return False
    async with httpx.AsyncClient(timeout=10) as client:
        for attempt in range(3):
            try:
                r = await client.post(WEBHOOK_URL, json={"alerts": alerts}, timeout=10)
                r.raise_for_status()
                return True
            except Exception as e:
                logger.warning("Webhook attempt %s failed: %s", attempt + 1, e)
                await asyncio.sleep(2 ** attempt)
    logger.error("Webhook failed after retries")
    return False

def _send_email_sync(alert: dict):
    # simple SMTP email, synchronous; offload to executor
    import smtplib
    from email.message import EmailMessage
    if not EMAIL_USER or not EMAIL_PASSWORD or not EMAIL_FROM:
        logger.warning("Email not configured; skipping email dispatch")
        return
    msg = EmailMessage()
    subject = f"ALERT {alert.get('alert_level')}: {alert.get('anomaly_type')}"
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(ADMIN_EMAILS)
    body = f"""Alert Level: {alert.get('alert_level')}
Type: {alert.get('anomaly_type')}
Tourist: {alert.get('tourist_id')}
Location: {alert.get('location')}
Time: {alert.get('timestamp')}
Confidence: {alert.get('confidence_score')}
"""
    msg.set_content(body)
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as s:
            s.starttls()
            s.login(EMAIL_USER, EMAIL_PASSWORD)
            s.send_message(msg)
        logger.info("Email sent for alert %s", alert.get("alert_id"))
    except Exception as e:
        logger.error("Failed to send email: %s", e)

async def _send_sms_async(alert: dict):
    if not (TWILIO_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM):
        logger.warning("Twilio not configured; skipping SMS")
        return
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        body = f"ALERT {alert.get('alert_level')}: {alert.get('anomaly_type')} at {alert.get('location')}"
        for p in ADMIN_PHONE:
            try:
                client.messages.create(body=body, from_=TWILIO_FROM, to=p)
            except Exception as e:
                logger.error("Twilio send failed for %s: %s", p, e)
        logger.info("SMS attempts complete for alert %s", alert.get("alert_id"))
    except Exception as e:
        logger.error("Twilio client error: %s", e)

async def dispatch_alert_background(alert: dict):
    """
    Called in background tasks. Handles webhook/email/sms per severity.
    """
    actions = SEVERITY_ACTIONS.get(alert.get("alert_level", "INFO"), ["log"])

    # Webhook (async with retries)
    if "webhook" in actions and WEBHOOK_URL:
        await _post_webhook([alert])

    # Email (run sync email in executor)
    if "email" in actions:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _send_email_sync, alert)

    # SMS (async Twilio)
    if "sms" in actions:
        await _send_sms_async(alert)

    logger.info("Dispatch finished for alert %s actions=%s", alert.get("alert_id"), actions)
