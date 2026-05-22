import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Consolidação M. Dias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
:root {
    --bg: #f5f7fa;
    --surface: #ffffff;
    --surface-soft: #f8fafc;
    --text: #111827;
    --muted: #64748b;
    --line: #e2e8f0;
    --line-strong: #cbd5e1;
    --primary: #1f5eff;
    --primary-dark: #1747c8;
    --success: #15803d;
    --warning: #b45309;
    --danger: #b91c1c;
    --radius: 12px;
}

html, body, [class*="css"] {
    font-family: Inter, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background:
        linear-gradient(180deg, #f8fafc 0%, #f5f7fa 32%, #f5f7fa 100%);
    color: var(--text);
}

.block-container {
    max-width: 1240px;
    padding: 32px 40px 28px;
}

h1, h2, h3, p {
    letter-spacing: 0;
}

h2 {
    color: var(--text) !important;
    font-size: 21px !important;
    line-height: 1.25 !important;
    font-weight: 750 !important;
    margin: 0 0 16px !important;
}

h3 {
    color: var(--text) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] > div {
    padding: 28px 20px;
}

section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 26px;
}

.brand-mark {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: grid;
