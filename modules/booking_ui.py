from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

import streamlit as st


def _to_date(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            return date.today()
    return date.today()


def _calculate_nights(start_date: date, end_date: date) -> int:
    return max(1, (end_date - start_date).days)


def _build_cart(trip_input: dict, selected_transport: dict | None, selected_hotel: dict | None) -> dict:
    travelers = int(trip_input.get("traveler_count", 1) or 1)
    start_date = _to_date(trip_input.get("start_date"))
    end_date = _to_date(trip_input.get("end_date"))
    nights = _calculate_nights(start_date, end_date)

    transport_total = 0.0
    if selected_transport:
        transport_total = float(selected_transport.get("price_per_traveler", 0)) * travelers

    hotel_total = 0.0
    if selected_hotel:
        hotel_total = float(selected_hotel.get("price_per_night", 0)) * nights

    return {
        "transport": selected_transport,
        "hotel": selected_hotel,
        "travelers": travelers,
        "nights": nights,
        "transport_total": round(transport_total, 2),
        "hotel_total": round(hotel_total, 2),
        "total_cost": round(transport_total + hotel_total, 2),
    }


def _create_payment_request(total_cost: float) -> dict:
    payment_id = f"PAY-{uuid4().hex[:10].upper()}"
    return {
        "payment_id": payment_id,
        "payment_link": f"https://payments.local/simulate/{payment_id}?amount={total_cost}",
        "status": "pending",
        "method": None,
    }


def render_booking_page() -> None:
    st.header("🛒 Booking Flow")
    st.caption("Review your selections and initiate the booking process.")

    trip_input = st.session_state.trip_input
    if not trip_input:
        st.info("📝 Please complete **Trip Creation** first.")
        return

    selected_transport = st.session_state.selected_transport
    selected_hotel = st.session_state.selected_hotel

    # ── Selected items ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🚆 Transportation")
        if selected_transport:
            st.metric("Provider", selected_transport.get("provider", "N/A"))
            st.metric("Type", selected_transport.get("type", "N/A"))
            st.metric("Price/Traveler", f"${selected_transport.get('price_per_traveler', 0)}")
        else:
            st.warning("No transport selected. Go to **Transport** page to choose.")

    with col2:
        st.markdown("### 🏨 Hotel")
        if selected_hotel:
            st.metric("Hotel", selected_hotel.get("name", "N/A"))
            st.metric("Location", selected_hotel.get("location", "N/A"))
            st.metric("Price/Night", f"${selected_hotel.get('price_per_night', 0)}")
        else:
            st.warning("No hotel selected. Go to **Hotels** page to choose.")

    # ── Cost breakdown preview ──
    if selected_transport or selected_hotel:
        st.divider()
        preview_cart = _build_cart(trip_input, selected_transport, selected_hotel)

        st.markdown("### 💰 Cost Breakdown")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 Travelers", preview_cart["travelers"])
        c2.metric("🌙 Nights", preview_cart["nights"])
        c3.metric("🚆 Transport", f"${preview_cart['transport_total']}")
        c4.metric("🏨 Hotel", f"${preview_cart['hotel_total']}")

        st.markdown(f"### 🧾 Total: **${preview_cart['total_cost']}**")

        st.divider()
        if st.button("💳 Initiate Booking Request", type="primary", use_container_width=True):
            cart = _build_cart(trip_input, selected_transport, selected_hotel)
            st.session_state.cart = cart
            st.session_state.payment = _create_payment_request(cart["total_cost"])
            st.session_state.current_page = "Payment"
            st.rerun()
    else:
        st.divider()
        st.error("❌ Select at least one item (transport or hotel) before booking.")
