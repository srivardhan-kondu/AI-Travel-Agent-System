from __future__ import annotations

import streamlit as st

from services.ai_service import chatbot_reply


SUGGESTED_QUESTIONS = [
    "What's the best time to visit?",
    "Recommend local food spots",
    "How should I budget my trip?",
    "What are the must-see attractions?",
    "Any safety tips for travelers?",
]


def render_chatbot_page() -> None:
    st.header("🤖 AI Travel Chatbot")
    st.caption("Ask destination questions, get travel tips, or refine your itinerary.")

    col_clear, _ = st.columns([1, 4])
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # ── Welcome message if empty ──
    if not st.session_state.chat_history:
        st.divider()
        st.markdown("### 👋 Hello! I'm your AI travel assistant.")

        destination = st.session_state.trip_input.get("destination", "")
        if destination:
            st.write(f"I see you're planning a trip to **{destination.title()}**! Feel free to ask me anything about your destination, itinerary, budget, food, safety, and more.")
        else:
            st.write("I can help you with destination info, travel tips, budgeting, local food, attractions, and more. Set up your trip details first for personalized answers!")

        st.markdown("**💡 Try asking:**")
        cols = st.columns(min(3, len(SUGGESTED_QUESTIONS)))
        for i, question in enumerate(SUGGESTED_QUESTIONS[:3]):
            with cols[i]:
                if st.button(f"💬 {question}", key=f"suggest_{i}", use_container_width=True):
                    st.session_state._pending_question = question
                    st.rerun()

        cols2 = st.columns(min(2, len(SUGGESTED_QUESTIONS[3:])))
        for i, question in enumerate(SUGGESTED_QUESTIONS[3:]):
            with cols2[i]:
                if st.button(f"💬 {question}", key=f"suggest_{i+3}", use_container_width=True):
                    st.session_state._pending_question = question
                    st.rerun()

        st.divider()

    # ── Render chat history ──
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Handle pending question from suggestion buttons ──
    pending = st.session_state.get("_pending_question", "")
    if pending:
        st.session_state._pending_question = ""
        user_message = pending
    else:
        user_message = st.chat_input("Ask a travel question...")

    if not user_message:
        return

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = chatbot_reply(
                user_message,
                st.session_state.itinerary,
                st.session_state.trip_input,
                st.session_state.chat_history,
            )
        st.markdown(answer)

    st.session_state.chat_history.append({"role": "user", "content": user_message})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
