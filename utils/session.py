import streamlit as st


DEFAULT_SESSION_STATE = {
    "is_authenticated": False,
    "auth_token": None,
    "current_user": {},
    "users": [],
    "current_page": "Trip Planner",
    "trip_input": {},
    "itinerary": {},
    "transport_options": [],
    "selected_transport": None,
    "hotel_options": [],
    "selected_hotel": None,
    "cart": {
        "transport": None,
        "hotel": None,
        "transport_total": 0.0,
        "hotel_total": 0.0,
        "total_cost": 0.0,
    },
    "payment": {
        "payment_id": None,
        "payment_link": None,
        "status": "idle",
        "method": None,
    },
    "bookings": [],
    "chat_history": [],
    "local_transport": [],
}


def init_session_state() -> None:
    """Initialise global session keys. Loads persisted users & bookings on first run."""
    for key, default_value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    # Load persisted data only once per session (guard with a sentinel key)
    if not st.session_state.get("_persistence_loaded"):
        try:
            from utils.persistence import load_persistent_state
            saved = load_persistent_state()
            # Merge: only overwrite users/bookings if they haven't been set yet
            if not st.session_state["users"] and saved["users"]:
                st.session_state["users"] = saved["users"]
            if not st.session_state["bookings"] and saved["bookings"]:
                st.session_state["bookings"] = saved["bookings"]
        except Exception:
            pass
        st.session_state["_persistence_loaded"] = True
