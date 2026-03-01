from __future__ import annotations

from datetime import date, datetime

import pandas as pd
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


def _cancel_booking(booking_id: str) -> None:
    """Mark a booking as cancelled and update payment status to refunded."""
    for booking in st.session_state.bookings:
        if booking["booking_id"] == booking_id:
            booking["booking_status"] = "cancelled"
            booking["payment"]["status"] = "refunded"
            break
    # Persist the updated state
    try:
        from utils.persistence import save_persistent_state
        save_persistent_state()
    except Exception:
        pass


def _booking_badge(booking_status: str, trip_end: date, today: date) -> str:
    if booking_status == "cancelled":
        return "🔴 Cancelled"
    if trip_end >= today:
        return "🟢 Upcoming"
    return "⚪ Past"


def render_dashboard_page() -> None:
    st.header("📊 Bookings Dashboard")
    st.caption("View your booking history, analytics, and trip details.")

    bookings = st.session_state.bookings
    if not bookings:
        st.info("📭 No bookings yet. Complete a payment to see your booking history.")
        return

    today = date.today()
    upcoming = []
    past = []
    cancelled = []

    for booking in bookings:
        status = booking.get("booking_status", "confirmed")
        trip_end = _to_date(booking["trip"]["end_date"])
        if status == "cancelled":
            cancelled.append(booking)
        elif trip_end >= today:
            upcoming.append(booking)
        else:
            past.append(booking)

    # ── Summary metrics ──
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📦 Total Bookings", len(bookings))
    c2.metric("🔜 Upcoming", len(upcoming))
    c3.metric("📁 Past", len(past))
    c4.metric("🔴 Cancelled", len(cancelled))
    total_spent = sum(
        b["payment"]["amount"]
        for b in bookings
        if b.get("booking_status") != "cancelled"
    )
    c5.metric("💰 Total Spent", f"${total_spent:,.2f}")

    st.divider()

    # ── Spending analytics ──
    active_bookings = [b for b in bookings if b.get("booking_status") != "cancelled"]
    if active_bookings:
        st.subheader("💰 Spending Analytics")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("**Spending by Destination**")
            dest_spending: dict[str, float] = {}
            for b in active_bookings:
                dest = b["trip"]["destination"]
                dest_spending[dest] = dest_spending.get(dest, 0) + b["payment"]["amount"]
            chart_df = pd.DataFrame({
                "Destination": list(dest_spending.keys()),
                "Amount (USD)": list(dest_spending.values()),
            })
            try:
                st.bar_chart(chart_df.set_index("Destination"))
            except TypeError:
                st.dataframe(chart_df, use_container_width=True, hide_index=True)

        with col_chart2:
            st.markdown("**Trips by Destination**")
            dest_counts: dict[str, int] = {}
            for b in active_bookings:
                dest = b["trip"]["destination"]
                dest_counts[dest] = dest_counts.get(dest, 0) + 1
            count_df = pd.DataFrame({
                "Destination": list(dest_counts.keys()),
                "Trips": list(dest_counts.values()),
            })
            try:
                st.bar_chart(count_df.set_index("Destination"))
            except TypeError:
                st.dataframe(count_df, use_container_width=True, hide_index=True)

    st.divider()

    # ── Bookings table ──
    st.subheader("📋 All Bookings")
    summary_rows = []
    for booking in bookings:
        trip_end = _to_date(booking["trip"]["end_date"])
        b_status = booking.get("booking_status", "confirmed")
        badge = _booking_badge(b_status, trip_end, today)
        summary_rows.append({
            "Status": badge,
            "Booking ID": booking["booking_id"],
            "Destination": booking["trip"]["destination"],
            "Dates": f"{booking['trip']['start_date']} → {booking['trip']['end_date']}",
            "Travelers": booking["trip"].get("travelers", 1),
            "Payment": f"${booking['payment']['amount']:,.2f}",
            "Method": booking["payment"].get("method", "N/A"),
            "Booking Status": b_status.title(),
        })

    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    # ── Booking detail cards ──
    st.divider()
    st.subheader("📂 Booking Details")
    for booking in bookings:
        trip_end = _to_date(booking["trip"]["end_date"])
        b_status = booking.get("booking_status", "confirmed")
        badge = _booking_badge(b_status, trip_end, today)

        with st.expander(f"{badge} | {booking['booking_id']} — {booking['trip']['destination']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🚆 Transport**")
                transport = booking.get("transport")
                if transport:
                    st.write(f"- **Type:** {transport.get('type', 'N/A')}")
                    st.write(f"- **Provider:** {transport.get('provider', 'N/A')}")
                    st.write(f"- **Time:** {transport.get('departure_time', '')} → {transport.get('arrival_time', '')}")
                else:
                    st.caption("No transport booked.")

            with c2:
                st.markdown("**🏨 Hotel**")
                hotel = booking.get("hotel")
                if hotel:
                    st.write(f"- **Name:** {hotel.get('name', 'N/A')}")
                    st.write(f"- **Location:** {hotel.get('location', 'N/A')}")
                    st.write(f"- **Price/Night:** ${hotel.get('price_per_night', 0)}")
                else:
                    st.caption("No hotel booked.")

            st.markdown("**💳 Payment**")
            pay = booking.get("payment", {})
            p1, p2, p3 = st.columns(3)
            p1.metric("Amount", f"${pay.get('amount', 0):,.2f}")
            p2.metric("Method", pay.get("method", "N/A"))
            p3.metric("Status", pay.get("status", "N/A").title())

            # ── Cancel button ──
            if b_status != "cancelled":
                st.divider()
                if st.button(
                    "🗑️ Cancel Booking",
                    key=f"cancel_{booking['booking_id']}",
                    type="secondary",
                    use_container_width=True,
                ):
                    _cancel_booking(booking["booking_id"])
                    st.success(f"✅ Booking **{booking['booking_id']}** has been cancelled and marked as refunded.")
                    st.rerun()
            else:
                st.warning("🔴 This booking has been cancelled. Payment has been refunded.")
