from dotenv import load_dotenv
import streamlit as st

from modules.auth_ui import render_auth_page
from modules.booking_ui import render_booking_page
from modules.chatbot_ui import render_chatbot_page
from modules.dashboard_ui import render_dashboard_page
from modules.hotel_ui import render_hotel_page
from modules.itinerary_ui import render_itinerary_page
from modules.payment_ui import render_payment_page
from modules.transport_ui import render_transport_page
from modules.trip_input_ui import render_trip_input_page
from utils.auth import is_authenticated, logout_user
from utils.config import get_openai_api_key
from utils.session import init_session_state
from utils.styles import inject_custom_css


PAGES = [
    "Trip Planner",
    "Itinerary",
    "Transport",
    "Hotels",
    "Booking",
    "Payment",
    "Dashboard",
    "Chatbot",
]

PAGE_ICONS = {
    "Trip Planner": "✈️",
    "Itinerary": "🗺️",
    "Transport": "🚆",
    "Hotels": "🏨",
    "Booking": "🛒",
    "Payment": "💳",
    "Dashboard": "📊",
    "Chatbot": "🤖",
}

load_dotenv()
st.set_page_config(page_title="AI Travel Agent", page_icon="🧳", layout="wide")
inject_custom_css()
init_session_state()

if not is_authenticated():
    render_auth_page()
    st.stop()

st.sidebar.markdown("## 🧳 AI Travel Agent")
st.sidebar.divider()
st.sidebar.success(f"👤 {st.session_state.current_user.get('email', 'Unknown')}")
token_preview = str(st.session_state.auth_token)[:12] if st.session_state.auth_token else "N/A"
st.sidebar.caption(f"🔑 Session: {token_preview}...")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout_user()
    st.rerun()

st.sidebar.divider()

if st.session_state.current_page not in PAGES:
    st.session_state.current_page = "Trip Planner"

selected_page = st.sidebar.radio(
    "Navigate",
    PAGES,
    index=PAGES.index(st.session_state.current_page),
    format_func=lambda p: f"{PAGE_ICONS.get(p, '')} {p}",
)
st.session_state.current_page = selected_page

if not get_openai_api_key():
    st.warning("OPENAI_API_KEY is not set. AI features will run with mock fallback responses.")

if selected_page == "Trip Planner":
    render_trip_input_page()
elif selected_page == "Itinerary":
    render_itinerary_page()
elif selected_page == "Transport":
    render_transport_page()
elif selected_page == "Hotels":
    render_hotel_page()
elif selected_page == "Booking":
    render_booking_page()
elif selected_page == "Payment":
    render_payment_page()
elif selected_page == "Dashboard":
    render_dashboard_page()
elif selected_page == "Chatbot":
    render_chatbot_page()
