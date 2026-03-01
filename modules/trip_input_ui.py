from __future__ import annotations

import re
from datetime import date, timedelta

import streamlit as st


POPULAR_DESTINATIONS = ["Paris", "Tokyo", "Bali", "London", "New York", "Rome", "Barcelona", "Dubai", "Singapore", "Sydney"]


def _is_valid_destination(destination: str) -> bool:
    destination = destination.strip()
    if len(destination) < 2:
        return False
    pattern = r"^[A-Za-z\u00C0-\u024F][A-Za-z\u00C0-\u024F\s\-'.,]+$"
    return bool(re.match(pattern, destination))


def _reset_booking_flow() -> None:
    st.session_state.itinerary = {}
    st.session_state.transport_options = []
    st.session_state.selected_transport = None
    st.session_state.hotel_options = []
    st.session_state.selected_hotel = None
    st.session_state.cart = {
        "transport": None,
        "hotel": None,
        "transport_total": 0.0,
        "hotel_total": 0.0,
        "total_cost": 0.0,
    }
    st.session_state.payment = {
        "payment_id": None,
        "payment_link": None,
        "status": "idle",
        "method": None,
    }


def render_trip_input_page() -> None:
    st.header("✈️ Trip Creation")
    st.caption("Set up your travel details. The AI will use these to craft your perfect itinerary.")
    st.divider()

    # ── Popular destinations ──
    st.markdown("**🌍 Popular Destinations**")
    cols = st.columns(5)
    for i, dest in enumerate(POPULAR_DESTINATIONS[:5]):
        with cols[i]:
            if st.button(dest, key=f"dest_{dest}", use_container_width=True):
                st.session_state._quick_dest = dest
    cols2 = st.columns(5)
    for i, dest in enumerate(POPULAR_DESTINATIONS[5:]):
        with cols2[i]:
            if st.button(dest, key=f"dest_{dest}", use_container_width=True):
                st.session_state._quick_dest = dest

    st.markdown("")

    # ── Form ──
    existing = st.session_state.trip_input
    today = date.today()

    quick_dest = st.session_state.get("_quick_dest", "")
    default_dest = quick_dest or existing.get("destination", "")
    default_source = existing.get("source_location", "")

    default_start = existing.get("start_date", today + timedelta(days=7))
    default_end = existing.get("end_date", today + timedelta(days=10))
    default_travelers = int(existing.get("traveler_count", 1) or 1)
    default_budget = existing.get("budget_range", "Not specified")
    default_prefs = existing.get("preferences", [])

    with st.form("trip_input_form"):
        col_src, col_dst = st.columns(2)
        with col_src:
            source_location = st.text_input(
                "📍 Traveling From * (city or country)",
                value=default_source,
                placeholder="e.g., Hyderabad, Mumbai, London...",
            )
            st.caption("Enter a city or country name using letters only.")
        with col_dst:
            destination = st.text_input(
                "🏙️ Destination * (city or country)",
                value=default_dest,
                placeholder="e.g., Paris, Tokyo, Dubai...",
            )
            st.caption("Enter your travel destination using letters only.")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date *", value=default_start, min_value=today)
        with col2:
            end_date = st.date_input("End Date *", value=default_end, min_value=today)

        col3, col4 = st.columns(2)
        with col3:
            traveler_count = st.number_input(
                "Number of Travelers",
                min_value=1, max_value=20,
                value=default_travelers, step=1,
            )
        with col4:
            budget_range = st.selectbox(
                "Budget Range",
                options=["Not specified", "Budget", "Mid-range", "Luxury"],
                index=["Not specified", "Budget", "Mid-range", "Luxury"].index(default_budget)
                if default_budget in {"Not specified", "Budget", "Mid-range", "Luxury"}
                else 0,
            )

        preferences = st.multiselect(
            "Travel Preferences",
            ["Adventure", "Relaxation", "Food", "Nightlife", "Culture", "Nature", "Shopping", "Family-friendly"],
            default=default_prefs,
        )
        submit = st.form_submit_button("💾 Save Trip Details", type="primary", use_container_width=True)

    if submit:
        if not source_location.strip():
            st.error("❌ Source location is required. Enter a city or country name.")
            return
        if not destination.strip():
            st.error("❌ Destination is required. Enter a city or country name.")
            return
        if not _is_valid_destination(source_location):
            st.error("❌ Invalid source location. Use only letters, spaces, and hyphens (e.g., 'New York', 'Paris').")
            return
        if not _is_valid_destination(destination):
            st.error("❌ Invalid destination. Use only letters, spaces, and hyphens (e.g., 'Tokyo', 'Bali').")
            return
        if end_date < start_date:
            st.error("❌ End date must be on or after start date.")
            return

        st.session_state.trip_input = {
            "source_location": source_location.strip(),
            "destination": destination.strip(),
            "start_date": start_date,
            "end_date": end_date,
            "traveler_count": int(traveler_count),
            "budget_range": budget_range,
            "preferences": preferences,
        }
        st.session_state._quick_dest = ""
        _reset_booking_flow()
        st.success("✅ Trip details saved! Head to **Itinerary** to generate your AI-powered travel plan.")

    # ── Current trip summary ──
    if st.session_state.trip_input:
        data = st.session_state.trip_input
        st.divider()
        st.subheader("📋 Current Trip Summary")

        days = ((data.get("end_date", today) - data.get("start_date", today)).days) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("📍 From", data.get("source_location", "").title())
        c2.metric("🏙️ To", data.get("destination", "").title())
        c3.metric("📅 Duration", f"{days} day{'s' if days != 1 else ''}")
        c4.metric("👥 Travelers", data.get("traveler_count", 1))
        c5.metric("💰 Budget", data.get("budget_range", "N/A"))

        prefs = data.get("preferences", [])
        if prefs:
            st.caption(f"**Preferences:** {', '.join(prefs)}")
