from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import streamlit as st


def _booking_exists(payment_id: str) -> bool:
    for booking in st.session_state.bookings:
        if booking.get("payment", {}).get("payment_id") == payment_id:
            return True
    return False


PAYMENT_ICONS = {
    "Credit Card": "💳",
    "UPI": "📱",
    "Net Banking": "🏦",
    "Wallet": "👛",
}


def render_payment_page() -> None:
    st.header("💳 Payment Simulation")
    st.caption("Complete your payment to confirm the booking.")

    cart = st.session_state.cart
    payment = st.session_state.payment
    trip_input = st.session_state.trip_input

    if not payment.get("payment_id"):
        st.info("🛒 No pending payment. Create a **Booking Request** first.")
        return

    # ── Already completed ──
    if payment.get("status") == "completed":
        st.success("✅ Payment completed! Your booking is confirmed.")
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Payment ID", payment.get("payment_id", ""))
        c2.metric("Method", f"{PAYMENT_ICONS.get(payment.get('method', ''), '')} {payment.get('method', 'N/A')}")
        c3.metric("Status", "✅ Completed")
        st.divider()
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        return

    # ── Itemized receipt ──
    st.markdown("### 🧾 Itemized Receipt")

    transport = cart.get("transport")
    hotel = cart.get("hotel")

    receipt_items = []
    if transport:
        receipt_items.append({
            "Item": f"🚆 {transport.get('type', 'Transport')} — {transport.get('provider', 'N/A')}",
            "Details": f"{transport.get('departure_time', '')} → {transport.get('arrival_time', '')}",
            "Amount (USD)": cart.get("transport_total", 0.0),
        })
    if hotel:
        receipt_items.append({
            "Item": f"🏨 {hotel.get('name', 'Hotel')}",
            "Details": f"{cart.get('nights', 0)} night(s) × ${hotel.get('price_per_night', 0)}",
            "Amount (USD)": cart.get("hotel_total", 0.0),
        })

    if receipt_items:
        import pandas as pd
        st.dataframe(pd.DataFrame(receipt_items), use_container_width=True, hide_index=True)

    # ── Total ──
    st.markdown(f"### 💰 Total: **${cart.get('total_cost', 0.0):,.2f}**")
    st.caption(f"Payment ID: `{payment.get('payment_id', '')}`")

    st.divider()

    # ── Payment method ──
    st.markdown("### 💳 Select Payment Method")
    methods = ["Credit Card", "UPI", "Net Banking", "Wallet"]
    cols = st.columns(len(methods))
    if "selected_method" not in st.session_state:
        st.session_state.selected_method = "Credit Card"

    for i, method in enumerate(methods):
        with cols[i]:
            icon = PAYMENT_ICONS.get(method, "")
            is_selected = st.session_state.selected_method == method
            label = f"{'✅ ' if is_selected else ''}{icon} {method}"
            if st.button(label, key=f"pay_method_{method}", use_container_width=True):
                st.session_state.selected_method = method
                st.rerun()

    method = st.session_state.selected_method

    st.divider()
    if st.button("✅ Complete Payment", type="primary", use_container_width=True):
        payment_id = payment["payment_id"]
        if _booking_exists(payment_id):
            st.session_state.payment["status"] = "completed"
            st.session_state.payment["method"] = method
            st.rerun()
            return

        booking = {
            "booking_id": f"BK-{uuid4().hex[:8].upper()}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "user_email": st.session_state.current_user.get("email", "unknown"),
            "trip": {
                "destination": trip_input.get("destination"),
                "start_date": str(trip_input.get("start_date")),
                "end_date": str(trip_input.get("end_date")),
                "travelers": cart.get("travelers", 1),
            },
            "transport": cart.get("transport"),
            "hotel": cart.get("hotel"),
            "payment": {
                "payment_id": payment_id,
                "status": "completed",
                "method": method,
                "amount": cart.get("total_cost", 0.0),
            },
            "booking_status": "confirmed",
        }

        st.session_state.bookings.append(booking)
        st.session_state.payment["status"] = "completed"
        st.session_state.payment["method"] = method
        # Persist the new booking to disk
        try:
            from utils.persistence import save_persistent_state
            save_persistent_state()
        except Exception:
            pass
        st.balloons()
        st.rerun()
