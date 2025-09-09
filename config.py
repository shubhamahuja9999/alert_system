# config.py
import os

# Admin contacts (comma separated)
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "admin1@example.com").split(",")
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+911234567890").split(",")

# Optional webhook (POST {"alerts":[ ... ]})
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Demo flags
DEMO_RULES = os.getenv("DEMO_RULES", "0") in ("1", "true", "True")
DEMO_SPEED_KMH = float(os.getenv("DEMO_SPEED_KMH", "30.0"))

# Email config
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Twilio (optional)
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")

# Prisma reads DATABASE_URL from .env automatically
DATABASE_URL = os.getenv("DATABASE_URL")

# Map alert levels to actions
SEVERITY_ACTIONS = {
    "INFO": ["log"],
    "WARNING": ["log", "dashboard"],
    "CRITICAL": ["log", "dashboard", "email", "sms", "webhook"],
}
