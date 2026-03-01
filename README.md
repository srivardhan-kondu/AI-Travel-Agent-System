# AI Travel Agent System

Modular Streamlit application for a staged AI travel booking workflow.

## Phase 0 Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Required environment value in `.env`:

- `OPENAI_API_KEY`

Optional:

- `OPENAI_MODEL` (default target model for itinerary/chat features)
- `APP_ENV` (example: `development`)

## Run App

```bash
streamlit run app.py
```

## Current Project Structure

```text
.
├── app.py
├── data
│   ├── __init__.py
│   └── mock_data.py
├── modules
│   ├── __init__.py
│   ├── auth_ui.py
│   ├── booking_ui.py
│   ├── chatbot_ui.py
│   ├── dashboard_ui.py
│   ├── hotel_ui.py
│   ├── itinerary_ui.py
│   ├── payment_ui.py
│   ├── transport_ui.py
│   └── trip_input_ui.py
├── requirements.txt
├── services
│   ├── __init__.py
│   ├── ai_service.py
│   └── mock_backend.py
├── .env.example
├── README.md
└── utils
    ├── __init__.py
    ├── auth.py
    ├── config.py
    └── session.py
```

## Build Sequence

1. Project Setup
2. User Auth
3. Travel Input UI
4. AI Engine
5. Transport Module
6. Hotel Module
7. Booking System
8. Payment Sim
9. Dashboard
10. Chatbot
11. Integration & Testing

## Implemented Features

- User registration/login/logout with password hashing (`passlib`) and session token handling.
- Trip input form with destination/date validation.
- AI itinerary generation and itinerary editing with OpenAI + fallback logic.
- Destination/place image rendering with itinerary sections.
- Transport and hotel recommendation modules from mock backend data.
- Booking cart with total cost calculation.
- Payment simulation flow and booking confirmation.
- Dashboard for upcoming/past booking history.
- Chatbot with itinerary-aware responses.
