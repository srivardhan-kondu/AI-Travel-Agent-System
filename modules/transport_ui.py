from __future__ import annotations

import pandas as pd
import streamlit as st

from services.mock_backend import fetch_transport_options, fetch_local_transport


def render_transport_page() -> None:
    st.header("🚆 Transportation Suggestions")
    st.caption("Browse route-based transport and local transit options for your destination.")

    trip_input = st.session_state.trip_input
    if not trip_input:
        st.info("📝 Please complete **Trip Creation** first.")
        return

    source = trip_input.get("source_location", "").title()
    destination = trip_input.get("destination", "").title()

    if source and destination:
        st.markdown(f"**🛫 Route: {source} → {destination}**")

    # ── Fetch transport ──
    tab_route, tab_local = st.tabs(["🛫 Route Transport", "🚇 Local Transport"])

    with tab_route:
        if st.button("🔍 Fetch Route Transport", type="primary", use_container_width=True, key="fetch_route"):
            with st.spinner(f"🤖 AI is finding transport options from {source} to {destination}..."):
                st.session_state.transport_options = fetch_transport_options(trip_input)
                st.session_state.selected_transport = None
            st.rerun()

        options = st.session_state.transport_options
        if not options:
            st.info("👆 Click above to fetch available transport from your source to destination.")
        else:
            # ── Filter by type ──
            all_types = sorted(set(item["type"] for item in options))
            selected_types = st.multiselect("Filter by type", all_types, default=all_types, key="transport_filter")
            filtered = [item for item in options if item["type"] in selected_types]

            if not filtered:
                st.warning("No transport options match your filter.")
            else:
                # ── Display table ──
                table_df = pd.DataFrame(filtered)[
                    ["type", "provider", "price_per_traveler", "total_price", "departure_time", "arrival_time", "duration"]
                ]
                table_df = table_df.rename(columns={
                    "type": "🚗 Transport",
                    "provider": "🏢 Provider",
                    "price_per_traveler": "💲 Price/Traveler",
                    "total_price": "💰 Total Price",
                    "departure_time": "🕐 Departure",
                    "arrival_time": "🕐 Arrival",
                    "duration": "⏱️ Duration",
                })
                st.dataframe(table_df, use_container_width=True, hide_index=True)

                # ── Price comparison ──
                st.markdown("**💰 Price Comparison**")
                chart_data = pd.DataFrame({
                    "Provider": [f"{item['type']} - {item['provider']}" for item in filtered],
                    "Total Price (USD)": [item["total_price"] for item in filtered],
                })
                try:
                    st.bar_chart(chart_data.set_index("Provider"))
                except TypeError:
                    st.dataframe(chart_data, use_container_width=True, hide_index=True)

                # ── Selection ──
                st.divider()
                selected_id = st.radio(
                    "Select preferred transport",
                    [item["id"] for item in filtered],
                    format_func=lambda x: next(
                        (
                            f"{'✈️' if item['type']=='Flight' else '🚆' if item['type']=='Train' else '🚌'} {item['type']} | {item['provider']} | ${item['total_price']} | {item['departure_time']} → {item['arrival_time']}"
                            for item in filtered
                            if item["id"] == x
                        ),
                        x,
                    ),
                )

                if st.button("✅ Confirm Transport Selection", use_container_width=True):
                    st.session_state.selected_transport = next(
                        (item for item in options if item["id"] == selected_id), None,
                    )
                    if st.session_state.selected_transport:
                        st.success("✅ Transportation option confirmed!")
                        st.rerun()

            if st.session_state.selected_transport:
                sel = st.session_state.selected_transport
                st.divider()
                st.subheader("📌 Selected Transport")
                c1, c2, c3 = st.columns(3)
                c1.metric("Type", sel['type'])
                c2.metric("Provider", sel["provider"])
                c3.metric("Total Price", f"${sel['total_price']}")

    with tab_local:
        if st.button("🔍 Fetch Local Transport", type="primary", use_container_width=True, key="fetch_local"):
            with st.spinner(f"🤖 AI is finding local transport in {destination}..."):
                st.session_state.local_transport = fetch_local_transport(trip_input)
            st.rerun()

        local_options = st.session_state.get("local_transport", [])
        if not local_options:
            st.info(f"👆 Click above to discover local transport options in **{destination}**.")
        else:
            st.markdown(f"### 🚇 Getting Around {destination}")
            for lt in local_options:
                recommended = "⭐ " if lt.get("recommended") else ""
                icon = {"Metro": "🚇", "Bus": "🚌", "Taxi": "🚕", "Rickshaw": "🛺", "Tram": "🚊",
                        "Ferry": "⛴️", "Ride-share": "🚗"}.get(lt["type"], "🚆")
                with st.expander(f"{recommended}{icon} {lt['name']} ({lt['type']})"):
                    st.write(lt.get("description", ""))
                    st.caption(f"💰 Price: {lt.get('price_range', 'Varies')}")
                    if lt.get("recommended"):
                        st.success("⭐ Recommended for tourists!")
