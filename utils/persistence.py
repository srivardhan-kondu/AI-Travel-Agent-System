"""
Persistence utilities for the AI Travel Agent.
Saves and loads users and bookings to/from a local JSON file so data
survives Streamlit server restarts.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import streamlit as st

# Stored alongside the mock_data directory so it's always within the project
_DATA_DIR = Path(__file__).parent.parent / "data"
_STORE_FILE = _DATA_DIR / "app_data.json"


def _default_serialiser(obj: Any) -> str:
    """JSON serialiser for date/datetime objects."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serialisable")


def save_persistent_state() -> None:
    """Persist users and bookings from session_state to JSON on disk."""
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "users": st.session_state.get("users", []),
            "bookings": st.session_state.get("bookings", []),
        }
        with open(_STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, default=_default_serialiser, indent=2)
    except Exception:
        # Never crash the app because a save failed
        pass


def load_persistent_state() -> dict[str, list]:
    """Load users and bookings from disk. Returns empty lists if file absent."""
    if not _STORE_FILE.exists():
        return {"users": [], "bookings": []}
    try:
        with open(_STORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "users": data.get("users", []),
            "bookings": data.get("bookings", []),
        }
    except Exception:
        return {"users": [], "bookings": []}
