from __future__ import annotations

CUSTOM_CSS = """
<style>
/* ─── Google Font ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

/* ─── Page header gradient ─── */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg, #0E1117 0%, #1A1F2E 100%);
}

/* ─── Sidebar styling ─── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0E1117 100%);
    border-right: 1px solid rgba(108, 99, 255, 0.15);
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 6px 12px;
    border-radius: 8px;
    transition: background 0.2s ease;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(108, 99, 255, 0.1);
}

/* ─── Metric cards ─── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1A1F2E 0%, #232B3E 100%);
    border: 1px solid rgba(108, 99, 255, 0.2);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

div[data-testid="stMetric"] label {
    color: #8B92A5 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #6C63FF !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}

/* ─── Buttons ─── */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    letter-spacing: 0.02em;
    transition: all 0.25s ease;
    border: 1px solid rgba(108, 99, 255, 0.3);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(108, 99, 255, 0.3);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6C63FF 0%, #5A52D5 100%);
    color: white;
    border: none;
}

/* ─── Expanders ─── */
details[data-testid="stExpander"] {
    background: #1A1F2E;
    border: 1px solid rgba(108, 99, 255, 0.12);
    border-radius: 12px;
    margin-bottom: 8px;
}

/* ─── Dataframes ─── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ─── Forms ─── */
div[data-testid="stForm"] {
    background: #1A1F2E;
    border: 1px solid rgba(108, 99, 255, 0.15);
    border-radius: 14px;
    padding: 24px;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 600;
    padding: 10px 24px;
}

/* ─── Chat messages ─── */
div[data-testid="stChatMessage"] {
    border-radius: 14px;
    border: 1px solid rgba(108, 99, 255, 0.08);
    margin-bottom: 6px;
}

/* ─── Images ─── */
img {
    border-radius: 12px;
}

/* ─── Success / Warning / Error / Info boxes ─── */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ─── Divider ─── */
hr {
    border-color: rgba(108, 99, 255, 0.15);
}

/* ─── Badge utility ─── */
.badge-ai {
    display: inline-block;
    background: linear-gradient(135deg, #6C63FF, #9F97FF);
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.badge-mock {
    display: inline-block;
    background: rgba(255, 193, 7, 0.2);
    color: #FFC107;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}

/* ─── Stat card helper ─── */
.stat-card {
    background: linear-gradient(135deg, #1A1F2E, #232B3E);
    border: 1px solid rgba(108, 99, 255, 0.15);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.stat-card h3 {
    color: #6C63FF;
    margin: 0;
    font-size: 1.8rem;
}
.stat-card p {
    color: #8B92A5;
    margin: 4px 0 0 0;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
</style>
"""


def inject_custom_css() -> None:
    """Inject premium CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
