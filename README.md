<div align="center">

# 🧳 AI Travel Agent System

**An intelligent, end-to-end travel planning application powered by OpenAI**

Plan trips · Generate AI itineraries · Book transport & hotels · Chat with an AI assistant

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.43-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Application Workflow](#-application-workflow)
- [Module Documentation](#-module-documentation)
- [API Integration](#-api-integration)
- [Data Management](#-data-management)
- [Security](#-security)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

The **AI Travel Agent System** is a full-stack, modular web application that simulates a complete travel booking experience. It leverages **OpenAI's GPT models** to generate personalised travel itineraries, provide destination recommendations, and power an intelligent travel chatbot — all within an elegant dark-themed Streamlit interface.

The system covers the entire travel planning lifecycle:

> **Register → Plan Trip → Generate AI Itinerary → Browse Transport & Hotels → Book → Pay → Manage Bookings → Chat with AI**

---

## ✨ Key Features

### 🔐 Authentication & Account Management
- Secure user registration and login with **PBKDF2-HMAC-SHA256** password hashing (260,000 iterations)
- Token-based session management with `secrets.token_urlsafe`
- Route protection — unauthenticated users cannot access any page
- **Persistent accounts** — user data survives app restarts via JSON storage

### ✈️ Smart Trip Planning
- Interactive trip creation form with destination, dates, budget, and preference inputs
- **10 popular destination** quick-select buttons
- Source and destination location validation with descriptive error messages
- Support for **13 curated destinations** with high-quality imagery

### 🤖 AI-Powered Itinerary Generation
- Full itinerary generation using **OpenAI GPT-4o-mini** (configurable)
- Day-by-day plans with morning, afternoon, and evening activities
- **Natural language editing** — modify itineraries by simply describing changes
- Estimated cost calculation per trip
- Graceful **mock fallback** when no API key is configured

### 🚆 Transportation Suggestions
- **Route-based transport** (source → destination): Flights, Trains, Buses
- **Local transport** at destination: Metro, Taxi, Tram, Ferry, Ride-share
- LLM-generated transport options for **any destination worldwide**
- Price comparison bar charts and type-based filtering
- Per-traveler and total price calculations

### 🏨 Hotel Recommendations
- Hotel cards with images, ratings (★), amenities, and pricing
- **Budget-aware filtering** (Budget / Mid-range / Luxury)
- LLM-generated hotel options for destinations beyond the curated set
- **Safe image rendering** — broken or hallucinated image URLs fall back gracefully
- Table comparison view

### 💳 Booking & Payment Simulation
- Cart system combining selected transport + hotel with cost breakdown
- Simulated payment gateway with 4 payment methods (Credit Card, UPI, Net Banking, Wallet)
- Unique Payment ID and Booking ID generation
- Booking confirmation with animated celebration

### 📊 Bookings Dashboard
- **Upcoming**, **Past**, and **Cancelled** booking tracking
- Spending analytics with destination-based bar charts
- Detailed booking cards with transport, hotel, and payment info
- **Cancel booking** functionality with automatic refund status update
- Persistent bookings that survive server restarts

### 💬 AI Travel Chatbot
- Context-aware conversational assistant powered by OpenAI
- References current itinerary and trip details automatically
- Pre-loaded suggested questions for quick interaction
- Rolling chat history (last 6 messages) for conversation continuity
- Keyword-based fallback responses when API is unavailable

### 🖼️ Clean, Image-Free Interface
- All pages render without images for a **fast, lightweight experience**
- Hotel cards display name, star rating, amenities, and pricing in a clean card layout
- Itinerary recommended places shown as readable text pills (`Place A · Place B · Place C`)
- No broken image risks — zero external image dependencies

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                       │
│                         (Streamlit UI)                          │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Auth UI  │ │ Trip     │ │Itinerary │ │ Chatbot  │          │
│  │          │ │ Input UI │ │ UI       │ │ UI       │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │Transport │ │ Hotel    │ │ Booking  │ │ Payment  │          │
│  │ UI       │ │ UI       │ │ UI       │ │ UI       │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │              Dashboard UI                        │          │
│  └──────────────────────────────────────────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                        SERVICE LAYER                            │
│                                                                 │
│  ┌─────────────────────────┐  ┌─────────────────────────┐      │
│  │     AI Service          │  │    Mock Backend          │      │
│  │  • Itinerary Gen        │  │  • Transport Fetch       │      │
│  │  • Itinerary Edit       │  │  • Hotel Fetch           │      │
│  │  • Chatbot Reply        │  │  • Budget Filtering      │      │
│  │  • Transport Gen (LLM)  │  │  • Fallback Logic        │      │
│  │  • Hotel Gen (LLM)      │  │                          │      │
│  │  • Local Transport Gen  │  │                          │      │
│  └────────────┬────────────┘  └────────────┬────────────┘      │
│               │                             │                   │
├───────────────┼─────────────────────────────┼───────────────────┤
│               ▼                             ▼                   │
│                         DATA LAYER                              │
│                                                                 │
│  ┌─────────────────────────┐  ┌─────────────────────────┐      │
│  │     Mock Data           │  │    Persistence           │      │
│  │  • Transport Records    │  │  • JSON File Storage     │      │
│  │  • Hotel Records        │  │  • User Accounts         │      │
│  │  • Destination Images   │  │  • Booking History       │      │
│  │  • Place Images (35+)   │  │  • Auto-save on Events   │      │
│  └─────────────────────────┘  └─────────────────────────┘      │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                      UTILITIES LAYER                            │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │  Auth    │ │  Config  │ │ Session  │ │  Styles  │          │
│  │ (PBKDF2)│ │ (env)    │ │ (state)  │ │ (CSS)    │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    EXTERNAL SERVICES                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────┐           │
│  │              OpenAI API (GPT-4o-mini)            │           │
│  │  • Chat Completions (JSON mode)                  │           │
│  │  • Itinerary / Transport / Hotel / Chat          │           │
│  └─────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
User Input ──► Trip Form ──► AI Service ──► OpenAI API
                                │                │
                                │         (JSON Response)
                                │                │
                                ▼                ▼
                          Mock Backend ◄── Sanitized Data
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              Transport     Hotels     Itinerary
              Options       Options    (Daily Plan)
                    │           │           │
                    ▼           ▼           ▼
                  Selection & Booking Cart
                           │
                           ▼
                    Payment Simulation
                           │
                           ▼
                   Booking Confirmed
                   (Persisted to JSON)
                           │
                           ▼
                    Dashboard Display
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit 1.43 | Interactive web UI with widgets, forms, charts |
| **AI Engine** | OpenAI GPT-4o-mini | Itinerary generation, editing, chatbot, data generation |
| **Language** | Python 3.10+ | Core application logic |
| **Data Processing** | Pandas 2.2 | Table rendering, data manipulation |
| **Environment** | python-dotenv 1.0 | Secure API key management |
| **Storage** | JSON File | Persistent user and booking data |
| **Security** | hashlib (PBKDF2) | Password hashing with cryptographic salt |
| **Styling** | Custom CSS | Dark theme, glassmorphism, responsive design |

---

## 📂 Project Structure

```
AI-Travel-Agent-System/
│
├── app.py                          # Main entry point — routing, sidebar, auth gate
│
├── modules/                        # UI Layer — one file per page
│   ├── __init__.py
│   ├── auth_ui.py                  # Login & Registration forms
│   ├── trip_input_ui.py            # Trip creation form with validation
│   ├── itinerary_ui.py             # AI itinerary display & editing
│   ├── transport_ui.py             # Transport browsing & selection
│   ├── hotel_ui.py                 # Hotel recommendations & selection
│   ├── booking_ui.py               # Cart & booking initiation
│   ├── payment_ui.py               # Payment simulation flow
│   ├── dashboard_ui.py             # Booking history & analytics
│   └── chatbot_ui.py               # AI travel chatbot
│
├── services/                       # Business Logic Layer
│   ├── __init__.py
│   ├── ai_service.py               # OpenAI integration (itinerary, chat, LLM data)
│   └── mock_backend.py             # Simulated backend API (transport, hotels)
│
├── data/                           # Data Layer
│   ├── __init__.py
│   ├── mock_data.py                # Static datasets, image URLs, place mappings
│   └── app_data.json               # Auto-generated persistent storage (users, bookings)
│
├── utils/                          # Shared Utilities
│   ├── __init__.py
│   ├── auth.py                     # Password hashing, login/register/logout logic
│   ├── config.py                   # Environment variable readers
│   ├── session.py                  # Streamlit session state initialisation
│   ├── persistence.py              # JSON save/load for data durability
│   └── styles.py                   # Custom CSS injection
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme & server configuration
│
├── .env.example                    # Template for environment variables
├── .env                            # Actual environment variables (git-ignored)
├── .gitignore                      # Git exclusion rules
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Check Command |
|---|---|---|
| **Python** | 3.10 or higher | `python3 --version` |
| **pip** | Latest | `pip3 --version` |
| **Git** | Any | `git --version` |
| **OpenAI API Key** | — | [Get one here](https://platform.openai.com/api-keys) *(optional — app works with mock data)* |

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/srivardhan-kondu/AI-Travel-Agent-System.git
cd AI-Travel-Agent-System
```

**2. Create and activate a virtual environment**

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

### Configuration

**4. Set up environment variables**

```bash
cp .env.example .env
```

Open `.env` in any text editor and add your API key:

```env
# Required for AI features (leave default for mock fallback mode)
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional — choose the OpenAI model (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Optional
APP_ENV=development
```

> **💡 No API Key?** No problem! The application works fully with intelligent mock/fallback data. You'll see a warning banner at the top, but every feature remains functional.

### Running the Application

**5. Start the Streamlit server**

```bash
streamlit run app.py
```

**6. Open in your browser**

The app will automatically open at:

```
http://localhost:8501
```

> **⚡ Quick Start Summary:**
> ```bash
> git clone https://github.com/srivardhan-kondu/AI-Travel-Agent-System.git
> cd AI-Travel-Agent-System
> python3 -m venv .venv && source .venv/bin/activate
> pip install -r requirements.txt
> cp .env.example .env
> # Edit .env with your OPENAI_API_KEY
> streamlit run app.py
> ```

---

## 🔄 Application Workflow

The system follows a linear, guided workflow:

```
Step 1          Step 2          Step 3          Step 4
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Register │───►│  Create  │───►│ Generate │───►│  Browse  │
│ / Login  │    │   Trip   │    │Itinerary │    │Transport │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
Step 8          Step 7          Step 6          Step 5 │
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Chat   │◄──│Dashboard │◄──│ Complete │◄──│   Book   │◄┘
│ with AI  │    │  View    │    │ Payment  │    │Transport │
└──────────┘    └──────────┘    └──────────┘    │ & Hotels │
                                                └──────────┘
```

| Step | Page | Description |
|---|---|---|
| 1 | **Auth** | Register a new account or log in with existing credentials |
| 2 | **Trip Planner** | Enter destination, dates, travelers, budget, and preferences |
| 3 | **Itinerary** | Generate an AI-powered day-by-day travel plan; edit with natural language |
| 4 | **Transport** | Browse and select route transport (flights, trains, buses) + local transit |
| 5 | **Hotels** | View hotel cards with images, ratings, amenities; select preferred hotel |
| 6 | **Booking** | Review cart with cost breakdown; initiate booking request |
| 7 | **Payment** | Choose payment method and complete simulated payment |
| 8 | **Dashboard** | View all bookings, spending analytics; cancel bookings if needed |
| ∞ | **Chatbot** | Ask travel questions anytime — the AI has your trip context |

---

## 📖 Module Documentation

### `app.py` — Application Entry Point
- Configures page settings (title, icon, wide layout)
- Loads environment variables and injects custom CSS
- Implements the auth gate: unauthenticated users see only the login page
- Renders the sidebar with navigation, user info, and logout button
- Routes to the selected page module

### `services/ai_service.py` — AI Engine
The core intelligence layer with 6 main functions:

| Function | Purpose | Fallback |
|---|---|---|
| `generate_itinerary()` | Creates a full daily itinerary from trip input | Mock itinerary with rotating places |
| `edit_itinerary()` | Modifies existing itinerary via natural language | Appends edit request to first day's note |
| `chatbot_reply()` | Answers travel questions with trip context | Keyword-based local response |
| `generate_transport_options()` | Produces route transport options via LLM | Single generic flight entry |
| `generate_local_transport()` | Generates in-city transit options via LLM | Single generic taxi entry |
| `generate_hotel_options()` | Creates hotel listings via LLM | First 3 static hotel records |

### `services/mock_backend.py` — Simulated Backend
Bridges the AI service and static data:
- Uses static data for known destinations (Paris, Tokyo, Bali)
- Falls back to LLM-generated data for unknown destinations
- Applies budget-based hotel filtering

### `utils/auth.py` — Authentication Engine
- `register_user()` — validates inputs, hashes password, stores user
- `login_user()` — verifies credentials, creates session token
- `logout_user()` — clears all session authentication state
- Uses PBKDF2-HMAC-SHA256 with 260,000 iterations and random 32-byte salt

### `utils/persistence.py` — Data Durability
- `save_persistent_state()` — writes users and bookings to `data/app_data.json`
- `load_persistent_state()` — reads them back on app startup
- Handles `date`/`datetime` serialisation automatically

---

## 🔌 API Integration

### OpenAI Integration

The system communicates with OpenAI via the official Python SDK:

```python
# All AI calls use JSON mode for structured responses
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.7,
    response_format={"type": "json_object"},
)
```

**Key Design Decisions:**
- **JSON mode** (`response_format`) ensures structured, parseable responses
- **Temperature 0.7** for creative itineraries; **0.4** for factual chatbot answers
- **Sanitisation layer** validates and normalises every LLM response before display
- **Graceful degradation** — every AI function has a complete mock fallback path

### Supported OpenAI Models

Set via `OPENAI_MODEL` in `.env`:

| Model | Cost | Quality | Recommended For |
|---|---|---|---|
| `gpt-4o-mini` | Low | Good | Default — best cost/quality balance |
| `gpt-4o` | Medium | Excellent | Higher quality itineraries |
| `gpt-4-turbo` | High | Excellent | Maximum quality |
| `gpt-3.5-turbo` | Very Low | Acceptable | Budget testing |

---

## 💾 Data Management

### Static Data (`data/mock_data.py`)

Pre-seeded datasets for **3 primary destinations** (Paris, Tokyo, Bali):

| Dataset | Records | Fields |
|---|---|---|
| `TRANSPORT_DATA` | 9 | id, destination, type, provider, price, times, duration |
| `HOTEL_DATA` | 9 | id, destination, name, price, rating, location, amenities, image |
| `DESTINATION_IMAGES` | 13 | Curated Unsplash URLs for destination hero banners |
| `PLACE_IMAGES` | 35 | Curated Unsplash URLs for landmark/attraction images |
| `DEFAULT_PLACES` | 11 | Default place lists per destination for fallback itineraries |

### Persistent Data (`data/app_data.json`)

Auto-generated JSON file storing:

```json
{
  "users": [
    {
      "user_id": "uuid",
      "email": "user@example.com",
      "password_hash": "salt:hash",
      "created_at": "ISO-8601"
    }
  ],
  "bookings": [
    {
      "booking_id": "BK-XXXXXXXX",
      "trip": { "destination": "...", "start_date": "...", "end_date": "..." },
      "transport": { "type": "...", "provider": "..." },
      "hotel": { "name": "...", "price_per_night": 0.0 },
      "payment": { "amount": 0.0, "status": "completed", "method": "..." },
      "booking_status": "confirmed"
    }
  ]
}
```

**Persistence triggers:**
- User registration → save
- User login → save  
- Payment completion → save
- Booking cancellation → save

---

## 🔒 Security

| Feature | Implementation |
|---|---|
| **Password Hashing** | PBKDF2-HMAC-SHA256, 260,000 iterations, 32-byte random salt |
| **Session Tokens** | `secrets.token_urlsafe(32)` — cryptographically secure |
| **Auth Gate** | `is_authenticated()` check before any page render |
| **API Key Protection** | `.env` file excluded from Git via `.gitignore` |
| **Input Validation** | Regex-based destination validation, date range checks, required field enforcement |
| **Safe Image Rendering** | URL validation with fallback — prevents broken images from untrusted LLM output |

---

## 📸 Screenshots

> Run the application locally to explore the full dark-themed UI with glassmorphism effects, animated charts, and rich media cards.

| Page | Description |
|---|---|
| 🔐 Login/Register | Dark-themed auth page with password strength indicator |
| ✈️ Trip Planner | Interactive form with popular destination quick-select |
| 🗺️ Itinerary | AI-generated daily plans with place images |
| 🚆 Transport | Route + local transport with price comparison charts |
| 🏨 Hotels | Hotel cards with images, ratings, and amenities |
| 💳 Payment | Itemized receipt with 4 payment method options |
| 📊 Dashboard | Booking history, spending analytics, cancel option |
| 🤖 Chatbot | Context-aware AI assistant with suggested questions |

---

## ❓ Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Activate virtual environment: `source .venv/bin/activate` |
| `OPENAI_API_KEY is not set` warning | Add your key to `.env` file, or ignore to use mock data |
| `openai.RateLimitError` | Reduce usage or upgrade your OpenAI plan |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
| Broken hotel images | This is handled automatically by the safe image fallback system |
| Data lost after restart | Check that `data/app_data.json` exists and has write permissions |
| `command not found: python` | Use `python3` instead of `python` on macOS/Linux |

---

## 🔮 Future Enhancements

- [ ] **Database Integration** — Migrate from JSON to SQLite/PostgreSQL for production readiness
- [ ] **Real API Integration** — Connect to Amadeus, Booking.com, or Skyscanner APIs
- [ ] **User Profile Management** — Editable profiles, travel preferences, saved destinations
- [ ] **Multi-language Support** — AI itineraries in user's preferred language
- [ ] **Email Notifications** — Booking confirmations and trip reminders
- [ ] **Social Features** — Share itineraries, group trip planning
- [ ] **Mobile Responsive Design** — Optimised layouts for mobile browsers
- [ ] **Advanced Analytics** — Travel trends, spending insights, recommendation engine
- [ ] **Offline Mode** — Cached itineraries accessible without internet

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "Add amazing feature"`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

Please ensure your code follows the existing module structure and includes appropriate fallback logic for AI-dependent features.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐** Star this repository if you found it helpful!

</div>
