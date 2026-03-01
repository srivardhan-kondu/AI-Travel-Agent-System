from __future__ import annotations

import streamlit as st

from services.ai_service import edit_itinerary, generate_itinerary


def _render_daily_plan(daily_plan: list[dict]) -> None:
    for day in daily_plan:
        title = day.get("title") or f"Day {day.get('day', '')}"
        with st.expander(f"📅 {title}", expanded=(day.get("day", 1) <= 2)):
            col_m, col_a, col_e = st.columns(3)
            with col_m:
                st.markdown("**🌅 Morning**")
                st.write(day.get("morning", ""))
            with col_a:
                st.markdown("**☀️ Afternoon**")
                st.write(day.get("afternoon", ""))
            with col_e:
                st.markdown("**🌙 Evening**")
                st.write(day.get("evening", ""))

            note = day.get("note")
            if note:
                st.caption(f"💡 {note}")

            places = day.get("places", [])
            if places:
                st.markdown("**📍 Recommended Places**")
                st.write(" · ".join(places))


def render_itinerary_page() -> None:
    st.header("🗺️ AI Itinerary Generation")
    st.caption("Generate a personalized travel plan using AI, then refine it with natural language requests.")

    trip_input = st.session_state.trip_input
    if not trip_input:
        st.info("📝 Please complete **Trip Creation** first to set up your travel details.")
        return

    destination = trip_input.get("destination", "")

    # ── Generate button ──
    col1, col2 = st.columns([3, 1])
    with col1:
        generate = st.button("🤖 Generate Itinerary", type="primary", use_container_width=True)
    with col2:
        if st.session_state.itinerary:
            regenerate = st.button("🔄 Regenerate", use_container_width=True)
        else:
            regenerate = False

    if generate or regenerate:
        with st.spinner("🧠 AI is crafting your personalized itinerary..."):
            st.session_state.itinerary = generate_itinerary(trip_input)
        st.success("✅ Itinerary generated successfully!")
        st.rerun()

    # ── Display itinerary ──
    itinerary = st.session_state.itinerary
    if itinerary:
        st.divider()

        # Source badge
        source = itinerary.get("source", "unknown")
        if source == "openai":
            st.markdown('<span class="badge-ai">🤖 AI-Generated</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-mock">📦 Mock Data</span>', unsafe_allow_html=True)

        st.subheader(f"📍 {itinerary.get('destination', destination.title())}")
        st.write(itinerary.get("overview", ""))

        # ── Cost & stats ──
        days = len(itinerary.get("daily_plan", []))
        cost = itinerary.get("estimated_total_cost", 0)
        currency = itinerary.get("currency", "USD")

        c1, c2, c3 = st.columns(3)
        c1.metric("📅 Days", days)
        c2.metric("💰 Estimated Cost", f"{currency} {cost:,.2f}")
        c3.metric("💵 Per Day", f"{currency} {cost / max(1, days):,.2f}")

        st.divider()
        _render_daily_plan(itinerary.get("daily_plan", []))

        # ── Edit form ──
        st.divider()
        st.markdown("### ✏️ Modify Itinerary")
        st.caption("Describe your changes in plain English — the AI will adjust your plan accordingly.")
        with st.form("edit_itinerary_form"):
            edit_request = st.text_area(
                "What would you like to change?",
                placeholder="Example: Make day 2 more family-friendly and include museum time.",
            )
            edit_submit = st.form_submit_button("✨ Apply Changes", type="primary", use_container_width=True)

        if edit_submit:
            if not edit_request.strip():
                st.error("❌ Please enter a modification request.")
                return
            with st.spinner("🔄 Updating itinerary..."):
                st.session_state.itinerary = edit_itinerary(itinerary, edit_request, trip_input)
            st.success("✅ Itinerary updated.")
            st.rerun()

        # ── Navigation shortcut ──
        st.divider()
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("🚆 Proceed to Transport →", use_container_width=True):
                st.session_state.current_page = "Transport"
                st.rerun()
        with col_nav2:
            if st.button("🏨 Proceed to Hotels →", use_container_width=True):
                st.session_state.current_page = "Hotels"
                st.rerun()
    else:
        st.info("👆 Click **Generate Itinerary** to create your AI-powered travel plan.")
