from __future__ import annotations

import pandas as pd
import streamlit as st

from services.mock_backend import fetch_hotel_options


def _star_rating(rating: float) -> str:
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "⭐" * full + ("✨" if half else "") + ("☆" * empty) + f" ({rating})"


def render_hotel_page() -> None:
    st.header("🏨 Hotel Recommendations")
    st.caption("Browse, compare, and select the perfect hotel for your stay.")

    trip_input = st.session_state.trip_input
    if not trip_input:
        st.info("📝 Please complete **Trip Creation** first.")
        return

    if st.button("🔍 Fetch Hotel Options", type="primary", use_container_width=True):
        st.session_state.hotel_options = fetch_hotel_options(trip_input)
        st.session_state.selected_hotel = None
        st.rerun()

    options = st.session_state.hotel_options
    if not options:
        st.info("👆 Click above to fetch hotel recommendations.")
        return

    # ── Hotel cards (no images) ──
    st.markdown("### 🏩 Available Hotels")
    for item in options:
        with st.container():
            col_info, col_price = st.columns([3, 1])
            with col_info:
                st.markdown(f"**{item['name']}**")
                st.write(f"📍 {item['location']} | {_star_rating(item['rating'])}")
                amenities = item.get("amenities", [])
                if amenities:
                    st.caption(f"🏷️ {', '.join(amenities)}")
            with col_price:
                st.metric("Price/Night", f"${item['price_per_night']}")
            st.divider()

    # ── Data table ──
    df = pd.DataFrame(options)[["name", "price_per_night", "rating", "location", "amenities"]]
    df = df.rename(columns={
        "name": "🏨 Hotel",
        "price_per_night": "💲 Price/Night",
        "rating": "⭐ Rating",
        "location": "📍 Location",
        "amenities": "🏷️ Amenities",
    })
    with st.expander("📊 Compare in Table View"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Selection ──
    st.divider()
    selected_id = st.radio(
        "Select preferred hotel",
        [item["id"] for item in options],
        format_func=lambda x: next(
            (
                f"🏨 {item['name']} | ${item['price_per_night']}/night | {_star_rating(item['rating'])} | {item['location']}"
                for item in options
                if item["id"] == x
            ),
            x,
        ),
    )

    if st.button("✅ Confirm Hotel Selection", use_container_width=True):
        st.session_state.selected_hotel = next(
            (item for item in options if item["id"] == selected_id), None,
        )
        if st.session_state.selected_hotel:
            st.success("✅ Hotel confirmed!")
            st.rerun()

    selected_hotel = st.session_state.selected_hotel
    if selected_hotel:
        st.divider()
        st.subheader("📌 Selected Hotel")
        c1, c2, c3 = st.columns(3)
        c1.metric("Hotel", selected_hotel["name"])
        c2.metric("Price/Night", f"${selected_hotel['price_per_night']}")
        c3.metric("Rating", _star_rating(selected_hotel["rating"]))
        st.info(f"📍 {selected_hotel.get('location', '')} | 🏷️ {', '.join(selected_hotel.get('amenities', []))}")
