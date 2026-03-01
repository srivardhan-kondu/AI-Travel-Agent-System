from __future__ import annotations

import streamlit as st

from utils.auth import login_user, register_user


def _password_strength(password: str) -> tuple[float, str, str]:
    """Return (progress 0-1, label, color) for password strength."""
    if not password:
        return 0.0, "", "gray"
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for c in password):
        score += 1

    levels = {0: ("Very Weak", "🔴"), 1: ("Weak", "🟠"), 2: ("Fair", "🟡"), 3: ("Good", "🟢"), 4: ("Strong", "🟢"), 5: ("Very Strong", "🟢")}
    label, icon = levels.get(score, ("", ""))
    return score / 5.0, f"{icon} {label}", "#4CAF50" if score >= 3 else "#FF9800" if score >= 2 else "#F44336"


def render_auth_page() -> None:
    st.markdown("## 🧳 AI Travel Agent")
    st.caption("Plan smarter. Travel better. Powered by AI.")
    st.divider()

    login_tab, register_tab = st.tabs(["🔑 Login", "📝 Create Account"])

    with login_tab:
        st.markdown("#### Welcome back!")
        st.caption("Log in to access your trips, bookings, and AI assistant.")
        with st.form("login_form", clear_on_submit=False):
            login_email = st.text_input("Email", key="login_email", placeholder="you@example.com")
            login_password = st.text_input("Password", type="password", key="login_password")
            login_submit = st.form_submit_button("Login", type="primary", use_container_width=True)

        if login_submit:
            if not login_email or not login_password:
                st.error("Please fill in both email and password.")
            else:
                success, message = login_user(login_email, login_password)
                if success:
                    st.success(message)
                    st.session_state.current_page = "Trip Planner"
                    st.rerun()
                else:
                    st.error(message)

    with register_tab:
        st.markdown("#### Create your account")
        st.caption("Set up your profile to start planning trips with AI assistance.")
        with st.form("register_form", clear_on_submit=True):
            reg_email = st.text_input("Email", key="reg_email", placeholder="you@example.com")
            reg_password = st.text_input("Password", type="password", key="reg_password")

            if reg_password:
                progress, label, color = _password_strength(reg_password)
                st.progress(progress, text=label)

            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

            st.caption("🔒 Password must be at least 8 characters.")
            register_submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if register_submit:
            success, message = register_user(reg_email, reg_password, reg_confirm)
            if success:
                st.success(f"✅ {message}")
                st.balloons()
            else:
                st.error(message)
