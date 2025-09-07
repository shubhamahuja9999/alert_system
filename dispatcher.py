# dispatcher.py
import smtplib
from config import ADMIN_EMAILS, ADMIN_PHONE, SEVERITY_ACTIONS

def send_email(alert):
    message = f"ALERT: {alert['alert_level']} - {alert['anomaly_type']} @ {alert['location']}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_password")  # 🔹 Replace creds
        for admin in ADMIN_EMAILS:
            server.sendmail("your_email@gmail.com", admin, message)

def send_sms(alert):
    from twilio.rest import Client
    client = Client("TWILIO_SID", "TWILIO_AUTH_TOKEN")
    for phone in ADMIN_PHONE:
        client.messages.create(
            body=f"CRITICAL ALERT: {alert['anomaly_type']} at {alert['location']}",
            from_="+1234567890", to=phone
        )

def dispatch_alert(alert):
    actions = SEVERITY_ACTIONS.get(alert["alert_level"], ["log"])
    if "email" in actions:
        send_email(alert)
    if "sms" in actions:
        send_sms(alert)
