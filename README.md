# 🔧 AppliFix — Voice AI Appliance Service System

> **An AI-powered voice agent that handles inbound phone calls for home appliance troubleshooting and technician scheduling — built with VAPI, Twilio, Groq, Deepgram, and FastAPI.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://postgresql.org)
[![VAPI](https://img.shields.io/badge/VAPI-Voice_AI-6366F1)](https://vapi.ai)
[![Twilio](https://img.shields.io/badge/Twilio-Phone-F22F46?logo=twilio&logoColor=white)](https://twilio.com)

---

## 📋 Overview

AppliFix is a **production-ready voice AI system** for Sears Home Services that accepts inbound phone calls and engages customers in natural voice conversation to:

1. **Diagnose appliance problems** — Identifies the appliance type, gathers symptoms, and provides step-by-step troubleshooting guidance for 6 appliance categories
2. **Schedule technician visits** — Finds available technicians by ZIP code and specialty, then books confirmed appointments
3. **Persist all data** — Every call, complaint, customer detail, and appointment is stored in PostgreSQL for operational tracking

The system handles the complete service lifecycle — from the moment a customer calls with a broken washer to having a confirmed technician appointment booked.

---

## 🏗️ Architecture

<p align="center">
  <img src="docs/AppliFix Architecture.png" alt="AppliFix Architecture Diagram" width="700" />
</p>

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Voice AI Platform** | [VAPI](https://vapi.ai) | Orchestrates the voice conversation, manages tool calls |
| **Phone Number** | [Twilio](https://twilio.com) | Provides the inbound US phone number |
| **Speech-to-Text** | [Deepgram Nova-2](https://deepgram.com) | Real-time speech recognition with smart formatting |
| **Text-to-Speech** | [Deepgram Aura](https://deepgram.com) | Ultra-low latency voice synthesis (~300ms) |
| **LLM** | [Groq — Llama 3.3 70B](https://groq.com) | Powers the conversational AI logic |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com) + Python 3.12 | REST API, webhook handling, business logic |
| **Database** | [PostgreSQL](https://postgresql.org) | Stores technicians, appointments, and call logs |
| **ORM** | [SQLAlchemy 2.0](https://sqlalchemy.org) | Database models and queries |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org) | Schema versioning and migrations |
| **Tunnel** | [ngrok](https://ngrok.com) | Exposes local backend to VAPI webhooks |

---

## 📞 Voice Agent Capabilities

### Tier 1 — Core Troubleshooting

The agent provides diagnostic guidance for **6 appliance types**:

| Appliance | Common Issues |
|-----------|--------------|
| 🧺 Washer | Not spinning, leaking, loud noise, won't start, error codes |
| 🔥 Dryer | Not heating, takes too long, loud noise, overheating |
| ❄️ Refrigerator | Not cooling, frost buildup, strange noises, water leaking |
| 🍽️ Dishwasher | Not cleaning, won't drain, door won't latch, leaking |
| 🍳 Oven | Not heating, uneven cooking, won't ignite, temperature issues |
| ❄️ HVAC | Not cooling/heating, strange noises, thermostat issues, airflow problems |

Each appliance has:
- **Quick troubleshooting checks** the agent walks the customer through
- **Severity classification** (urgent / moderate / minor) based on symptom keywords
- **Safety escalation** for dangerous symptoms (smoke, gas, sparks)

### Tier 2 — Technician Scheduling

- **10 seeded technicians** across 30 US ZIP codes
- ZIP-code + specialty matching to find the right technician
- **Available time slot presentation** (up to 3 options)
- Full appointment booking with verbal confirmation
- Appointment status tracking (confirmed → completed / cancelled)

---

## 🗄️ Database Schema

```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Technicians │────<│ Service Areas  │     │ Availability     │
│              │     │ (ZIP codes)   │     │ Slots            │
│ id           │     │ zip_code      │     │ day_of_week      │
│ name         │     └───────────────┘     │ date             │
│ email        │                           │ start_time       │
│ phone        │────<┌───────────────┐     │ end_time         │
│ is_active    │     │ Specialties   │     │ is_booked        │
└──────┬───────┘     │ appliance_type│     └──────────────────┘
       │             └───────────────┘
       │
       │         ┌───────────────────┐     ┌──────────────────┐
       └────────<│  Appointments     │     │  Call Logs        │
                 │ customer_name     │     │ call_id          │
                 │ customer_phone    │     │ caller_phone     │
                 │ customer_zip      │     │ appliance_type   │
                 │ appliance_type    │     │ zip_code         │
                 │ issue_description │     │ customer_name    │
                 │ scheduled_date    │     │ conversation_summary│
                 │ scheduled_time    │     │ status           │
                 │ status            │     │ started_at       │
                 │ call_id           │     │ ended_at         │
                 └───────────────────┘     └──────────────────┘
```

---

## ⚡ VAPI Tool Calls

The voice agent uses **4 server-side tools** that hit the backend webhook:

| # | Tool | Trigger | What It Does |
|---|------|---------|-------------|
| 1 | `get_troubleshooting_steps` | After identifying appliance + symptoms | Returns diagnostic steps and severity level |
| 2 | `find_technician` | After collecting ZIP code + appliance type | Queries DB for matching technicians with open slots |
| 3 | `book_appointment` | After customer verbally confirms a slot | Creates appointment record, marks slot as booked |
| 4 | `update_call_context` | Whenever name, ZIP, or appliance is learned | Silently updates the call log in background |

All tool calls route through a single webhook endpoint: `POST /vapi/webhook`

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- [ngrok](https://ngrok.com) account (free)
- [VAPI](https://vapi.ai) account (free $10 credit)
- [Twilio](https://twilio.com) account (for phone number)

### 1. Clone & Install

```bash
git clone <repository-url>
cd sears-home-services

# Create virtual environment
python -m venv backend/venv
source backend/venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/voice_ai_db

# VAPI
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
VAPI_ASSISTANT_ID=your_assistant_id

# App
BACKEND_URL=https://your-ngrok-url.ngrok-free.dev
```

### 3. Setup Database

```bash
# Create the PostgreSQL database
createdb voice_ai_db

# Tables are auto-created on first run, or use Alembic:
cd backend && alembic upgrade head && cd ..

# Seed technician data (10 technicians across 30 ZIP codes)
python scripts/seed_data.py
```

### 4. Start the Backend

```bash
source backend/venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Expose via ngrok

```bash
ngrok http 8000
# Copy the HTTPS URL → paste into .env as BACKEND_URL
# Also update all VAPI tool server URLs with this URL
```

### 6. Configure VAPI

1. Create an assistant in the VAPI dashboard
2. Set the **Model** to Groq → Llama 3.3 70B
3. Set the **Transcriber** to Deepgram Nova-2
4. Set the **Voice** to Deepgram Aura (`aura-asteria-en`)
5. Add all 4 tools with your ngrok webhook URL
6. Assign your Twilio phone number to the assistant

> 📖 See `VAPI_SETUP.md` for detailed step-by-step instructions with JSON configs for each tool.

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/vapi/webhook` | Receives all VAPI events and tool calls |
| `GET` | `/health` | Health check |

---

## 📁 Project Structure

```
sears-home-services/
├── main.py                          # FastAPI entry point
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (not committed)
├── .env.example                     # Template for environment variables
│
├── backend/
│   ├── config.py                    # Pydantic settings loader
│   ├── database/
│   │   ├── connection.py            # SQLAlchemy engine & Base
│   │   ├── session.py               # Database session dependency
│   │   └── models.py               # All ORM models (6 tables)
│   ├── models/
│   │   └── db_operations.py         # CRUD operations layer
│   ├── interactors/
│   │   ├── conversation_interactor.py   # VAPI webhook & tool call router
│   │   ├── troubleshooting_interactor.py # Diagnostic logic for 6 appliances
│   │   └── scheduling_interactor.py     # Technician search & booking logic
│   ├── routes/
│   │   ├── vapi_routes.py           # /vapi/* endpoints
│   │   ├── scheduling_routes.py     # /scheduling/* endpoints
│   │   └── health_routes.py         # /health endpoint
│   └── alembic/                     # Database migrations
│
└── scripts/
    ├── seed_data.py                 # Seeds 10 technicians + availability
    └── run_local.sh                 # Quick start script
```

---

## 🧪 Testing the Agent

### Test ZIP Codes (seeded technicians)

| ZIP Code | Technicians Available |
|----------|----------------------|
| 90210 | Carlos Rivera (washer, dryer, dishwasher) |
| 10001 | Amanda Chen (refrigerator, oven, hvac) |
| 60601 | Marcus Johnson (washer, oven, hvac) |
| 77001 | Priya Patel (refrigerator, washer, dryer) |
| 30301 | Derek Okafor (hvac, dryer, dishwasher) |
| 85001 | Sofia Hernandez (washer, refrigerator, oven) |
| 98101 | James Wilson (dryer, dishwasher, hvac) |
| 48201 | Lisa Park (washer, dryer, refrigerator) |
| 02101 | Robert Taylor (oven, hvac, dishwasher) |
| 94102 | Elena Volkov (washer, dryer, oven) |

### Sample Call Script

> **Agent:** Hello! You've reached AppliFix. What appliance is giving you trouble today?
>
> **You:** My washer is making a loud noise and won't spin.
>
> **Agent:** *(calls get_troubleshooting_steps)* I have some steps we can try. First, check if the washer lid is fully closed...
>
> **You:** I tried that, it's still not working. Can I get a technician?
>
> **Agent:** Sure! What's your ZIP code?
>
> **You:** 90210
>
> **Agent:** *(calls find_technician)* I found Carlos Rivera available Monday at 9 AM, Wednesday at 10 AM, or Friday at 9 AM. Which works best?
>
> **You:** Monday at 9 works. My name is Alex.
>
> **Agent:** *(calls book_appointment)* Your appointment is confirmed — Carlos Rivera will visit Monday at 9 AM for your washer at ZIP 90210. Is that correct?

---

## 🔑 Free Tier Summary

| Service | Free Allowance |
|---------|---------------|
| VAPI | $10 credit (~100 min of calls) |
| Deepgram | $200 credit — covers both STT and TTS |
| Groq | Free tier with rate limits |
| ngrok | Free (1 tunnel, random URL) |
| PostgreSQL (Neon) | Free tier (512 MB) |

---

## 📄 License

This project was built as a take-home assignment for **Sears Home Services**.
