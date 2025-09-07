# config.py

ADMIN_EMAILS = ["admin1@example.com"]
ADMIN_PHONE = ["+911234567890"]

# Postgres DB (loaded from .env by Prisma)

# Alert Severity Rules
SEVERITY_ACTIONS = {
    "INFO": ["log"],
    "WARNING": ["log", "dashboard"],
    "CRITICAL": ["log", "dashboard", "email", "sms"]
}
