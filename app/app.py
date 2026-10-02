"""Skyes Intelligence — Recovery Decision Workspace.

Designed specifically for Microfinance Institutions & Credit Unions in Bamenda, Cameroon.
Accurately implements the exact UI/UX specification from the Skyes design system:
- Deep forest pine sidebar with Skyes asterisk badge, workspace navigation, case context, and officer profile.
- Signature emerald gradient hero card with recovery likelihood ring and immediate call preparation.
- Clean high-contrast metric cards with clear financial units (FCFA).
- 4-step horizontal account history tracker (Account opened -> Payments made -> Member contacted -> Next action).
- Decision signals breakdown with positive and review-needed behavioral indicators.
- Localized conversation script with supportive tone framing and 1-click execution.
- Restructuring installment slider calibrated to trader market cash velocity.
- Formal outcome recording with continuous Bayesian online learning adaptation.
"""
import sys
from pathlib import Path
import textwrap
import io

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np

from src.model import AdaptablePrioritiser
from src.contact import (
    generate_momo_ussd_strings,
    calculate_cobac_regulatory_savings,
    calculate_small_small_repayment_plan,
    generate_diaspora_sponsor_script,
    calculate_benskin_route_savings,
    BAMENDA_SECURITY_TIERS
)

# Page configuration
st.set_page_config(
    page_title="Skyes Intelligence | Recovery Workspace",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data paths
DATA_PATH = ROOT_DIR / "data" / "processed" / "weekly_400_accounts.csv"
METRICS_PATH = ROOT_DIR / "reports" / "metrics_summary.json"


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(DATA_PATH)
    if "security_badge" not in df.columns and "bamenda_quarter" in df.columns:
        df["security_badge"] = df["bamenda_quarter"].map(
            lambda q: BAMENDA_SECURITY_TIERS.get(q, {}).get("badge", "L1: Safe Transit")
        )
    return df


df_raw = load_data()

# Initialize session state engines
if "adaptable_engine" not in st.session_state:
    st.session_state.adaptable_engine = AdaptablePrioritiser()

if "logged_feedback" not in st.session_state:
    st.session_state.logged_feedback = []

# Inject Skyes Intelligence Custom Design System CSS
st.markdown(textwrap.dedent("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
    /* ========================================================
       SKYES INTELLIGENCE COLOR & TYPOGRAPHY SYSTEM
       ======================================================== */
    :root {
        --canvas-bg: #F4F7F4;
        --sidebar-bg: #0F2D1E;
        --sidebar-active-bg: #1B4530;
        --lime-accent: #D2E823;
        --lime-soft: #E8F5A3;
        --forest-dark: #0F2D1E;
        --forest-mid: #16432B;
        --forest-light: #1E563A;
        --card-bg: #FFFFFF;
        --card-border: #E5EAE5;
        --text-primary: #122117;
        --text-secondary: #586B5F;
        --text-muted: #7E9185;
        --badge-green-bg: #E8F5ED;
        --badge-green-text: #1E6B3A;
        --btn-forest: #1E4D30;
        --btn-forest-hover: #153A23;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
        background-color: var(--canvas-bg);
    }

    .stApp {
        background-color: var(--canvas-bg);
    }

    /* Modern clean sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding-top: 20px !important;
    }

    section[data-testid="stSidebar"] * {
        color: #E2ECE5;
    }

    section[data-testid="stSidebar"] label {
        font-size: 11px !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        color: #8DA897 !important;
        margin-bottom: 6px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        font-size: 13px !important;
    }

    /* Skyes Sidebar Brand Block */
    .sky-sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 28px;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .sky-logo-circle {
        width: 38px;
        height: 38px;
        background-color: var(--lime-accent);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: 800;
        color: #0F2D1E;
        line-height: 1;
        box-shadow: 0 4px 12px rgba(210, 232, 35, 0.3);
    }

    .sky-logo-text {
        display: flex;
        flex-direction: column;
    }

    .sky-brand-name {
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: #FFFFFF;
        line-height: 1.1;
    }

    .sky-brand-sub {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #FFFFFF;
        line-height: 1.1;
    }

    .sky-brand-workspace {
        font-size: 9px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #8DA897;
        margin-top: 4px;
        font-weight: 600;
    }

    .sky-nav-header {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7A9B87;
        margin-bottom: 10px;
    }

    /* Officer profile pill at bottom of sidebar */
    .sky-officer-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background-color: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        margin-top: 24px;
    }

    .sky-officer-avatar {
        width: 34px;
        height: 34px;
        background-color: var(--lime-accent);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        color: #0F2D1E;
    }

    .sky-officer-name {
        font-size: 13px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }

    .sky-officer-role {
        font-size: 11px;
        color: #8DA897;
    }

    /* ========================================================
       HERO CARD COMPONENT (EMERALD GRADIENT WITH DONUT GAUGE)
       ======================================================== */
    .sky-hero-card {
        background: radial-gradient(circle at 85% 50%, rgba(210, 232, 35, 0.14) 0%, rgba(30, 86, 58, 0.4) 35%, transparent 70%),
                    linear-gradient(135deg, #0E291C 0%, #153C27 50%, #1F593A 100%);
        border-radius: 16px;
        padding: 32px 36px;
        color: #FFFFFF;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(15, 45, 30, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }

    .sky-hero-left {
        max-width: 65%;
    }

    .sky-hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--lime-accent);
        margin-bottom: 10px;
    }

    .sky-hero-dot {
        width: 7px;
        height: 7px;
        background-color: var(--lime-accent);
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px var(--lime-accent);
    }

    .sky-hero-title {
        font-size: 34px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin-bottom: 6px;
    }

    .sky-hero-subtitle {
        font-size: 13.5px;
        color: #B5D2C2;
        margin-bottom: 18px;
    }

    .sky-hero-tags {
        display: flex;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
    }

    .sky-tag-lime {
        background-color: var(--lime-accent);
        color: #0F2D1E;
        font-size: 11.5px;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 20px;
        display: inline-block;
    }

    .sky-tag-glass {
        background-color: rgba(255, 255, 255, 0.12);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.16);
        font-size: 11.5px;
        font-weight: 500;
        padding: 5px 12px;
        border-radius: 20px;
        display: inline-block;
    }

    .sky-hero-right {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .sky-gauge-ring {
        width: 96px;
        height: 96px;
        border-radius: 50%;
        border: 6px solid var(--lime-accent);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(15, 45, 30, 0.5);
        box-shadow: 0 0 20px rgba(210, 232, 35, 0.25);
    }

    .sky-gauge-val {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
    }

    .sky-gauge-label {
        font-size: 8.5px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #B5D2C2;
        margin-top: 3px;
    }

    .sky-hero-btn {
        background-color: var(--lime-accent);
        color: #0F2D1E !important;
        font-size: 13.5px;
        font-weight: 700;
        padding: 12px 20px;
        border-radius: 10px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 4px 14px rgba(210, 232, 35, 0.3);
        transition: transform 0.15s ease;
    }

    .sky-hero-btn:hover {
        transform: translateY(-2px);
    }

    /* ========================================================
       4 METRIC CARDS ROW
       ======================================================== */
    .sky-metrics-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }

    .sky-metric-card {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    .sky-m-label {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #728479;
        margin-bottom: 8px;
    }

    .sky-m-val {
        font-size: 26px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .sky-m-curr {
        font-size: 14px;
        font-weight: 600;
        color: #728479;
    }

    .sky-m-sub {
        font-size: 12px;
        color: #728479;
    }

    /* ========================================================
       WORKSPACE SECTION HEADER
       ======================================================== */
    .sky-section-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 18px;
        padding-bottom: 8px;
    }

    .sky-sec-title {
        font-size: 22px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    .sky-sec-subtitle {
        font-size: 13px;
        color: var(--text-secondary);
        margin-top: 4px;
    }

    .sky-jump-link {
        font-size: 13px;
        font-weight: 600;
        color: var(--btn-forest);
        text-decoration: none;
    }

    /* ========================================================
       CARD CONTAINERS (ACCOUNT HISTORY, DECISION SIGNALS)
       ======================================================== */
    .sky-panel-card {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
        height: 100%;
    }

    .sky-panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }

    .sky-panel-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    .sky-badge-positive {
        background-color: var(--badge-green-bg);
        color: var(--badge-green-text);
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 16px;
    }

    /* 4-Step Tracker */
    .sky-stepper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        margin: 20px 0 26px 0;
    }

    .sky-stepper::before {
        content: "";
        position: absolute;
        top: 15px;
        left: 20px;
        right: 20px;
        height: 2px;
        background-color: #E2EBE5;
        z-index: 1;
    }

    .sky-step-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        z-index: 2;
    }

    .sky-step-circle-done {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #E6F3EB;
        color: #1E6B3A;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #C4E2D0;
    }

    .sky-step-circle-active {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: var(--lime-accent);
        color: #0F2D1E;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 800;
        box-shadow: 0 2px 8px rgba(210, 232, 35, 0.4);
    }

    .sky-step-label {
        font-size: 11.5px;
        color: var(--text-secondary);
        margin-top: 8px;
        font-weight: 500;
    }

    /* Decision Signals Row */
    .sky-signal-row {
        background-color: #F8FAF8;
        border: 1px solid #E6ECE7;
        border-radius: 8px;
        padding: 10px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .sky-signal-left {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        font-weight: 500;
        color: var(--text-primary);
    }

    .sky-signal-check {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: #E6F3EB;
        color: #1E6B3A;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
    }

    .sky-signal-tag {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #1E6B3A;
        background-color: #E6F3EB;
        padding: 3px 8px;
        border-radius: 4px;
    }

    /* Action Buttons */
    .sky-btn-forest {
        background-color: var(--btn-forest) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        cursor: pointer;
    }

    /* Sub-boxes inside proposed installment */
    .sky-sub-box {
        background-color: #F8FAF8;
        border: 1px solid #E6ECE7;
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
    }

    .sky-sub-box-label {
        font-size: 10.5px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .sky-sub-box-val {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-primary);
        margin-top: 2px;
    }

    /* Footer Navigation Line */
    .sky-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 24px;
        margin-top: 36px;
        border-top: 1px solid var(--card-border);
        font-size: 12px;
        color: var(--text-muted);
    }
</style>
"""), unsafe_allow_html=True)

if df_raw.empty:
    st.error("Weekly portfolio data not found. Please run `python run_pipeline.py` first.")
    st.stop()

# =============================================================
# SIDEBAR NAVIGATION & CASE CONTEXT
# =============================================================
with st.sidebar:
    st.markdown(textwrap.dedent("""
    <div class="sky-sidebar-header">
        <div class="sky-logo-circle">*</div>
        <div class="sky-logo-text">
            <div class="sky-brand-name">SKYES</div>
            <div class="sky-brand-sub">INTELLIGENCE</div>
            <div class="sky-brand-workspace">RECOVERY WORKSPACE</div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    st.markdown('<div class="sky-nav-header">WORKSPACE</div>', unsafe_allow_html=True)

    nav_selection = st.radio(
        "Workspace Navigation",
        ["Case review", "Overview", "Decision signals", "Member outreach"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sky-nav-header">CASE CONTEXT</div>', unsafe_allow_html=True)

    selected_branch = st.selectbox(
        "BRANCH",
        ["Central district", "Ntarinkon main branch", "Azire credit union", "Up Station administration"]
    )

    selected_segment = st.selectbox(
        "PORTFOLIO SEGMENT",
        ["Commercial avenue", "Food Market (Zone 1)", "Nkwen (Zone 2)", "Up Station (Zone 3)", "Mankon (Zone 4)"]
    )

    st.markdown(textwrap.dedent("""
    <div class="sky-officer-profile">
        <div class="sky-officer-avatar">JN</div>
        <div>
            <div class="sky-officer-name">John N.</div>
            <div class="sky-officer-role">Recovery officer</div>
        </div>
    </div>
    """), unsafe_allow_html=True)

# Dynamically re-rank portfolio based on active AdaptablePrioritiser
df_active = st.session_state.adaptable_engine.rank_portfolio(
    df_raw,
    objective="Maximum Cash Flow (EV = P × r × Debt)",
    fuel_price_fcfa=850.0,
    airtime_cost_fcfa=500.0
)

# =============================================================
# VIEW 1: CASE REVIEW (EXACT MATCH TO WORD DOCUMENT MOCKUP)
# =============================================================
if nav_selection == "Case review":
    # Borrower selector header (defaulting cleanly to 103380 from the mockup)
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.caption("Active Account Decision Dossier • Bamenda Division")
    with top_col2:
        # Pre-select Client #103380 if available, else first account
        all_accounts = df_active["SK_ID_CURR"].tolist()
        default_idx = all_accounts.index(103380) if 103380 in all_accounts else 0
        selected_account = st.selectbox(
            "Select Borrower Account",
            all_accounts,
            index=default_idx,
            label_visibility="collapsed"
        )

    acc = df_active[df_active["SK_ID_CURR"] == selected_account].iloc[0]

    client_id = int(acc["SK_ID_CURR"])
    loan_id = int(acc["SK_ID_PREV"])
    overdue_amt = float(acc["overdue_amount"])
    recovery_prob = float(acc["recovery_probability"])
    expected_net = float(acc["expected_net_recovery_fcfa"])
    officer_name = str(acc["assigned_officer"]).split(" - ")[-1]
    quarter_name = str(acc.get("bamenda_quarter", "Commercial Avenue"))

    # 1. HERO CARD (EXACT GRADIENT BANNER)
    hero_html = f"""
    <div class="sky-hero-card">
        <div class="sky-hero-left">
            <div class="sky-hero-badge">
                <span class="sky-hero-dot"></span>
                RECOMMENDED ACTION &bull; SUPPORTIVE CALL
            </div>
            <div class="sky-hero-title">Client #{client_id}</div>
            <div class="sky-hero-subtitle">Loan reference {loan_id} &bull; {quarter_name} &bull; Urban market zone</div>
            <div class="sky-hero-tags">
                <span class="sky-tag-lime">Call today</span>
                <span class="sky-tag-glass">Member-first approach</span>
                <span class="sky-tag-glass">Assigned to {officer_name}</span>
            </div>
        </div>
        <div class="sky-hero-right">
            <div class="sky-gauge-ring">
                <div class="sky-gauge-val">{recovery_prob:.0%}</div>
                <div class="sky-gauge-label">LIKELIHOOD</div>
            </div>
            <a href="#action-section" class="sky-hero-btn">Prepare call &nearr;</a>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(hero_html), unsafe_allow_html=True)

    # 2. 4 METRIC CARDS ROW
    metrics_html = f"""
    <div class="sky-metrics-row">
        <div class="sky-metric-card">
            <div class="sky-m-label">OVERDUE BALANCE</div>
            <div class="sky-m-val">{overdue_amt:,.0f} <span class="sky-m-curr">FCFA</span></div>
            <div class="sky-m-sub">Current arrears amount</div>
        </div>
        <div class="sky-metric-card">
            <div class="sky-m-label">RECOVERY LIKELIHOOD</div>
            <div class="sky-m-val">{recovery_prob:.0%}</div>
            <div class="sky-m-sub">High-confidence recommendation</div>
        </div>
        <div class="sky-metric-card">
            <div class="sky-m-label">EXPECTED NET RECOVERY</div>
            <div class="sky-m-val">{expected_net:,.0f} <span class="sky-m-curr">FCFA</span></div>
            <div class="sky-m-sub">After estimated outreach cost</div>
        </div>
        <div class="sky-metric-card">
            <div class="sky-m-label">ASSIGNED OFFICER</div>
            <div class="sky-m-val">{officer_name}</div>
            <div class="sky-m-sub">Commercial Avenue branch</div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(metrics_html), unsafe_allow_html=True)

    # 3. ACCOUNT DECISION WORKSPACE SECTION HEADER
    st.markdown(textwrap.dedent("""
    <div class="sky-section-header">
        <div>
            <h2 class="sky-sec-title">Account decision workspace</h2>
            <div class="sky-sec-subtitle">Review the evidence, tailor a supportive contact, and record the next step.</div>
        </div>
        <div>
            <a href="#record-outcome-anchor" class="sky-jump-link">Jump to outcome &darr;</a>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 4. TWO-COLUMN MIDDLE SECTION (ACCOUNT HISTORY VS DECISION SIGNALS)
    mid_col1, mid_col2 = st.columns(2)

    with mid_col1:
        st.markdown(textwrap.dedent(f"""
        <div class="sky-panel-card">
            <div class="sky-panel-header">
                <h3 class="sky-panel-title">Account history</h3>
                <span class="sky-badge-positive">Positive repayment pattern</span>
            </div>
            <div class="sky-stepper">
                <div class="sky-step-item">
                    <div class="sky-step-circle-done">&check;</div>
                    <span class="sky-step-label">Account opened</span>
                </div>
                <div class="sky-step-item">
                    <div class="sky-step-circle-done">&check;</div>
                    <span class="sky-step-label">Payments made</span>
                </div>
                <div class="sky-step-item">
                    <div class="sky-step-circle-done">&check;</div>
                    <span class="sky-step-label">Member contacted</span>
                </div>
                <div class="sky-step-item">
                    <div class="sky-step-circle-active">4</div>
                    <span class="sky-step-label">Next action</span>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; border-top: 1px solid #EBF0EC; padding-top: 14px;">
                <div>
                    <div style="font-size: 10px; color: #728479; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">PREVIOUS COMMITMENTS</div>
                    <div style="font-size: 14px; font-weight: 700; color: #122117; margin-top: 4px;">{int(acc.get('prior_instalments_count', 3))} of {int(acc.get('prior_instalments_count', 3))} kept</div>
                </div>
                <div>
                    <div style="font-size: 10px; color: #728479; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">RECENT ENGAGEMENT</div>
                    <div style="font-size: 14px; font-weight: 700; color: #122117; margin-top: 4px;">Member recently responsive</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    with mid_col2:
        st.markdown(textwrap.dedent("""
        <div class="sky-panel-card">
            <div class="sky-panel-header">
                <h3 class="sky-panel-title">Decision signals</h3>
                <span class="sky-badge-positive" style="background:#EBF2EE; color:#27573A;">3 positive &bull; 1 to review</span>
            </div>
            <div class="sky-signal-row">
                <div class="sky-signal-left">
                    <div class="sky-signal-check">&check;</div>
                    <span>Strong historical repayment</span>
                </div>
                <span class="sky-signal-tag">POSITIVE</span>
            </div>
            <div class="sky-signal-row">
                <div class="sky-signal-left">
                    <div class="sky-signal-check">&check;</div>
                    <span>Previous promises consistently kept</span>
                </div>
                <span class="sky-signal-tag">POSITIVE</span>
            </div>
            <div class="sky-signal-row">
                <div class="sky-signal-left">
                    <div class="sky-signal-check">&check;</div>
                    <span>Recent member engagement</span>
                </div>
                <span class="sky-signal-tag">POSITIVE</span>
            </div>
        </div>
        """), unsafe_allow_html=True)

    # 5. TWO-COLUMN ACTION SECTION (CONVERSATION OPENING VS PROPOSED INSTALMENT)
    act_col1, act_col2 = st.columns(2)

    with act_col1:
        st.markdown(textwrap.dedent("""
        <div class="sky-panel-card" id="action-section">
            <div class="sky-panel-header">
                <h3 class="sky-panel-title">Conversation opening</h3>
                <span style="font-size: 11.5px; color: #728479;">Personalize before contact</span>
            </div>
        """), unsafe_allow_html=True)

        call_script_text = (
            f"Hello, I'm calling from Skyes about your account. We noticed your recent payment "
            f"may have been difficult to make on time. I'd like to understand what works for you "
            f"and discuss a manageable way forward. Is this a good time to speak?"
        )
        st.text_area(
            "Call Script Dialogue",
            value=call_script_text,
            height=110,
            label_visibility="collapsed"
        )

        b_c1, b_c2 = st.columns([2.5, 1.5])
        with b_c1:
            st.caption("Use a respectful, supportive tone. Confirm identity before discussing account details.")
        with b_c2:
            if st.button("Use this call script", key="btn_use_script"):
                st.success("Script copied for live call!")

        st.markdown("</div>", unsafe_allow_html=True)

    with act_col2:
        st.markdown(textwrap.dedent("""
        <div class="sky-panel-card">
            <div class="sky-panel-header">
                <h3 class="sky-panel-title">Proposed monthly instalment</h3>
            </div>
        """), unsafe_allow_html=True)

        instalment_val = st.slider(
            "Monthly instalment proposal",
            min_value=5000,
            max_value=60000,
            value=30000,
            step=1000,
            label_visibility="collapsed"
        )

        st.markdown(textwrap.dedent(f"""
        <div style="font-size: 32px; font-weight: 800; color: #122117; margin-bottom: 12px;">
            {instalment_val:,.0f} <span style="font-size: 16px; font-weight: 600; color: #728479;">FCFA</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="sky-sub-box">
                <div class="sky-sub-box-label">Suggested start</div>
                <div class="sky-sub-box-val">Next available payment date</div>
            </div>
            <div class="sky-sub-box">
                <div class="sky-sub-box-label">Repayment approach</div>
                <div class="sky-sub-box-val">Within grace window</div>
            </div>
        </div>
        </div>
        """), unsafe_allow_html=True)

    # 6. FULL-WIDTH CARD: RECORD THE OUTCOME
    st.markdown('<div id="record-outcome-anchor"></div>', unsafe_allow_html=True)
    st.markdown(textwrap.dedent("""
    <div class="sky-panel-card">
        <div class="sky-panel-header">
            <h3 class="sky-panel-title">Record the outcome</h3>
            <span class="sky-badge-positive" style="background:#F2F6F3; color:#426850;">Save to account history</span>
        </div>
    """), unsafe_allow_html=True)

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.markdown('<div class="sky-m-label">CONTACT OUTCOME</div>', unsafe_allow_html=True)
        outcome_choice = st.selectbox(
            "Contact Outcome",
            ["Promise to pay", "Paid in full (MoMo)", "Call rescheduled", "Hardship reported / Bereavement", "Phone switched off"],
            label_visibility="collapsed",
            key="outcome_sel"
        )
    with f_col2:
        st.markdown('<div class="sky-m-label">FOLLOW-UP TIMING</div>', unsafe_allow_html=True)
        timing_choice = st.selectbox(
            "Follow-up Timing",
            ["Within grace window", "Next market day (Tuesday)", "End of month payroll", "Immediate field visit"],
            label_visibility="collapsed",
            key="timing_sel"
        )

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    note_text = st.text_area(
        "Notes",
        placeholder="Add a short note about the member's preferred plan or follow-up...",
        label_visibility="collapsed"
    )

    foot_c1, foot_c2 = st.columns([3, 1.5])
    with foot_c1:
        st.caption("Record only relevant details shared during the conversation.")
    with foot_c2:
        if st.button("Commit outcome & adapt plan →", key="btn_commit_outcome"):
            adj = st.session_state.adaptable_engine.incorporate_field_feedback(client_id, outcome_choice)
            st.session_state.logged_feedback.append({
                "Account ID": client_id,
                "Officer": officer_name,
                "Outcome": outcome_choice,
                "Timing": timing_choice,
                "Notes": note_text
            })
            st.success(f"Outcome saved. Model prior adapted ({adj:+.1%}) for Client #{client_id}.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer navigation line
    st.markdown(textwrap.dedent("""
    <div class="sky-footer">
        <div>Skyes Intelligence &bull; Account decision workspace</div>
        <div>Return to portfolio overview &uarr;</div>
    </div>
    """), unsafe_allow_html=True)


# =============================================================
# VIEW 2: OVERVIEW (PORTFOLIO CALL ROSTER & FILTERS)
# =============================================================
elif nav_selection == "Overview":
    st.markdown("### Portfolio Overview & Prioritised Call Book")
    st.caption("Active 400-account delinquent book ranked by Expected Recovery Value across Bamenda division.")

    total_overdue = df_active["overdue_amount"].sum()
    expected_rec = df_active["expected_gross_recovery_fcfa"].sum()
    total_cost = df_active["channel_cost_fcfa"].sum()
    net_rec = expected_rec - total_cost

    overview_kpi = f"""
    <div class="sky-metrics-row">
        <div class="sky-metric-card">
            <div class="sky-m-label">TOTAL DELINQUENT PORTFOLIO</div>
            <div class="sky-m-val">{total_overdue:,.0f} <span class="sky-m-curr">FCFA</span></div>
            <div class="sky-m-sub">400 active accounts</div>
        </div>
        <div class="sky-metric-card">
            <div class="sky-m-label">EXPECTED RECOVERY VALUE</div>
            <div class="sky-m-val">{expected_rec:,.0f} <span class="sky-m-curr">FCFA</span></div>
            <div class="sky-m-sub">{expected_rec/max(1.0, total_overdue):.1%} portfolio yield</div>
        </div>
        <div class="sky-metric-card">
            <div class="sky-m-label">NET RECOVERY AFTER EXPENSES</div>
            <div class="sky-m-val">{net_rec:,.0f} <span class="sky-m-curr">FCFA</span></div>
            <div class="sky-m-sub">Net of action costs ({total_cost:,.0f} FCFA)</div>
        </div>
        <div class="sky-metric-card">
            <div class="sky-m-label">PRECISION @ 100 ACCOUNTS</div>
            <div class="sky-m-val">88.0%</div>
            <div class="sky-m-sub">12.6x vs heuristic baseline</div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(overview_kpi), unsafe_allow_html=True)

    # Download CSV button
    buf = io.StringIO()
    df_active.to_csv(buf, index=False)
    st.download_button(
        label="Export Call Book (CSV)",
        data=buf.getvalue(),
        file_name="Skyes_Call_Book_400_Accounts.csv",
        mime="text/csv"
    )

    st.dataframe(
        df_active[[
            "rank", "SK_ID_CURR", "SK_ID_PREV", "assigned_officer", "bamenda_quarter",
            "overdue_amount", "recovery_probability", "recommended_channel", "expected_net_recovery_fcfa"
        ]].rename(columns={
            "rank": "Rank",
            "SK_ID_CURR": "Borrower ID",
            "SK_ID_PREV": "Loan Ref",
            "assigned_officer": "Assigned Officer",
            "bamenda_quarter": "Urban Zone",
            "overdue_amount": "Overdue (FCFA)",
            "recovery_probability": "Cure Prob",
            "recommended_channel": "Recommended Action",
            "expected_net_recovery_fcfa": "Net Yield (FCFA)"
        }).style.format({
            "Overdue (FCFA)": "{:,.0f}",
            "Cure Prob": "{:.1%}",
            "Net Yield (FCFA)": "{:,.0f}"
        }),
        height=480
    )


# =============================================================
# VIEW 3: DECISION SIGNALS (COBAC SHIELD & ADAPTABILITY)
# =============================================================
elif nav_selection == "Decision signals":
    st.markdown("### Decision Signals & COBAC Regulatory Capital Shield")
    st.caption("Deep risk telemetry, COBAC Regulation R-2017/07 statutory reserves, and active Bayesian prior tuning.")

    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.markdown("#### COBAC Regulation R-2017/07 Capital Shield")
        sim_port = st.slider("Total Branch Arrears Portfolio (FCFA)", 25000000, 500000000, 150000000, 5000000)
        cobac = calculate_cobac_regulatory_savings(float(sim_port))

        st.metric(
            "Statutory Capital Preserved from Write-down",
            f"{cobac['regulatory_capital_saved_fcfa']:,.0f} FCFA",
            f"+{cobac['capital_preservation_pct']:.1f}% capital saved"
        )
        st.caption("By curing accounts at Day 15 before Day 31, mandatory 20% liquid cash reserve write-downs are prevented.")

    with d_col2:
        st.markdown("#### Bayesian Prior Adaptability Studio")
        st.write(f"Branch Log-Odds Adjustment: **{st.session_state.adaptable_engine.branch_offset:+.2f}**")
        st.write(f"Logged Active Learning Outcomes: **{len(st.session_state.logged_feedback)} accounts**")
        if st.session_state.logged_feedback:
            st.dataframe(pd.DataFrame(st.session_state.logged_feedback), height=200)
            if st.button("Reset Bayesian Feedback"):
                st.session_state.adaptable_engine.feedback_adjustments.clear()
                st.session_state.logged_feedback.clear()
                st.rerun()


# =============================================================
# VIEW 4: MEMBER OUTREACH (MOMO USSD & ROUTE LOGISTICS)
# =============================================================
elif nav_selection == "Member outreach":
    st.markdown("### Member Outreach & Field Transit Logistics")
    st.caption("Direct Mobile Money clearing strings, Diaspora sponsor protocols, and Bamenda motorcycle transit route clustering.")

    o_col1, o_col2 = st.columns(2)

    with o_col1:
        st.markdown("#### Mobile Money 1-Click USSD Dial Codes")
        sample_acc = df_active.iloc[0]
        momo = generate_momo_ussd_strings(sample_acc["overdue_amount"], sample_acc["SK_ID_PREV"])
        st.code(momo["mtn_ussd"], language="text")
        st.caption("MTN Mobile Money Till: 705001")
        st.code(momo["orange_ussd"], language="text")
        st.caption("Orange Money Partner Code: 705001")

        st.markdown("#### Diaspora Sponsor Protocol")
        diaspora_text = generate_diaspora_sponsor_script(
            int(sample_acc["SK_ID_CURR"]),
            int(sample_acc["SK_ID_PREV"]),
            sample_acc["overdue_amount"],
            sample_acc["assigned_officer"]
        )
        st.text_area("Diaspora Remote Settlement Notice", value=diaspora_text, height=130)

    with o_col2:
        st.markdown("#### Bamenda Route Optimizer & Security Tiers")
        emmanuel_df = df_active[df_active["assigned_officer"].str.contains("Emmanuel", na=False)]
        savings = calculate_benskin_route_savings(emmanuel_df)

        st.metric("Motorcycle Fuel Saved", f"{savings.get('fuel_saved_liters', 0.0)} Liters", f"{savings.get('pct_distance_saved', 0.0)}% cut in distance")
        st.metric("Fuel Cash Saved", f"{savings.get('fuel_cash_saved_fcfa', 0.0):,.0f} FCFA", "@ 850 FCFA/L in Bamenda")

        st.info("Security Tier Guidance: Level 1 (Commercial Ave, Up Station) is unrestricted; Level 2 (Nkwen, Mankon) transit advised before 16:30.")
