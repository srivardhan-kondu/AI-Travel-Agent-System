import hashlib
import os
import re
import secrets
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

import streamlit as st


def _hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a random salt."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=260000)
    return salt.hex() + ":" + key.hex()


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against its stored hash."""
    try:
        salt_hex, key_hex = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        actual_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=260000)
        return actual_key == expected_key
    except (ValueError, AttributeError):
        return False


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _validate_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, email))


def _find_user_by_email(email: str) -> Optional[dict]:
    normalized = _normalize_email(email)
    for user in st.session_state.users:
        if user["email"] == normalized:
            return user
    return None


def register_user(email: str, password: str, confirm_password: str) -> tuple[bool, str]:
    email = _normalize_email(email)

    if not email or not password or not confirm_password:
        return False, "All fields are required."
    if not _validate_email(email):
        return False, "Enter a valid email address."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if password != confirm_password:
        return False, "Passwords do not match."
    if _find_user_by_email(email):
        return False, "An account with this email already exists."

    st.session_state.users.append(
        {
            "user_id": str(uuid4()),
            "email": email,
            "password_hash": _hash_password(password),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    try:
        from utils.persistence import save_persistent_state
        save_persistent_state()
    except Exception:
        pass
    return True, "Registration successful. You can now log in."


def login_user(email: str, password: str) -> tuple[bool, str]:
    email = _normalize_email(email)
    user = _find_user_by_email(email)
    if not user:
        return False, "No account found for this email."

    if not _verify_password(password, user["password_hash"]):
        return False, "Invalid password."

    st.session_state.is_authenticated = True
    st.session_state.auth_token = secrets.token_urlsafe(32)
    st.session_state.current_user = {
        "user_id": user["user_id"],
        "email": user["email"],
        "login_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        from utils.persistence import save_persistent_state
        save_persistent_state()
    except Exception:
        pass
    return True, "Login successful."


def logout_user() -> None:
    st.session_state.is_authenticated = False
    st.session_state.auth_token = None
    st.session_state.current_user = {}
    st.session_state.current_page = "Trip Planner"


def is_authenticated() -> bool:
    return bool(st.session_state.is_authenticated and st.session_state.auth_token)
