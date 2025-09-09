# Alert System

A FastAPI-based alert system for processing and dispatching security alerts.

## Features

- FastAPI REST API for processing alerts
- PostgreSQL database with Prisma ORM
- Email and SMS notifications via Twilio
- Webhook support for external integrations
- Auto-reload development server

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Copy the example environment file and configure your settings:

```bash
copy .env.example .env
```

Edit `.env` with your database and notification settings.

### 3. Set Up Database

```bash
# Generate Prisma client
npx prisma generate

# Run database migrations
npx prisma db push
```

### 4. Run Development Server

**Option 1: Using the development script (Recommended)**
```bash
python dev.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using the batch file (Windows)**
```bash
run_dev.bat
```

**Option 4: Using the shell script (Linux/Mac)**
```bash
chmod +x run_dev.sh
./run_dev.sh
```

The server will start at `http://localhost:8000` with auto-reload enabled.

## API Endpoints

- `GET /health` - Health check
- `POST /process-alerts` - Process alert data
- `GET /alerts` - List all alerts
- `GET /alerts/{alert_id}` - Get specific alert

## Development

The development server (`dev.py`) includes:
- Auto-reload when code changes
- Detailed logging
- Access logs
- Hot reload for both Python files and Prisma schema

## Configuration

All configuration is done through environment variables in the `.env` file:

- `DATABASE_URL` - PostgreSQL connection string
- `ADMIN_EMAILS` - Comma-separated admin email addresses
- `ADMIN_PHONE` - Comma-separated admin phone numbers
- `EMAIL_*` - Email configuration for notifications
- `TWILIO_*` - Twilio configuration for SMS
- `WEBHOOK_URL` - External webhook endpoint

## Troubleshooting

If the site is not reloading:
1. Make sure you're using `python dev.py` or `uvicorn main:app --reload`
2. Check that you're not running the server without the `--reload` flag
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
