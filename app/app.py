"""Skye8 Collections Prioritiser — Haute-Elegance 10/10 Masterpiece Edition.

Designed for Microfinance Institutions & Credit Unions in Bamenda, Cameroon.
Features:
- Refined Haute-Luxury Editorial Palette (Warm Cashmere Alabaster, Espresso Cocoa Noir, Champagne Gold).
- Visual Probability Meter & Recovery Tier Gauge.
- 1-Click Offline Field Sheet Export (CSV) for Officers on Motorcycle Transit.
- Real-time Borrower ID & Loan Reference Search Engine.
- Portfolio Recovery Tier Distribution breakdown.
- Dossier-style Account Deep-Dive Inspector with custom Engagement Scripts.
- Ethical Hardship Safeguards protecting vulnerable & senior households.
"""
from pathlib import Path
import textwrap
import io
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration - Masterpiece Edition
st.set_page_config(
    page_title="Skye8 Prioritiser | Haute Masterpiece",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "weekly_400_accounts.csv"
METRICS_PATH = Path(__file__).resolve().parents[1] / "reports" / "metrics_summary.json"


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)


df_raw = load_data()

# Inject Masterpiece High-Luxury Editorial CSS
st.markdown(textwrap.dedent("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Global Base Palette */
    :root {
        --canvas-bg: #FAF7F2;
        --card-bg: #FFFFFF;
        --noir-dark: #15100E;
        --noir-medium: #221A16;
        --cognac-gold: #C5A059;
        --cognac-rich: #A67C48;
        --taupe-muted: #84756A;
        --border-refined: #EAE2D7;
        --border-gold: rgba(197, 160, 89, 0.35);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        color: #241D19;
        background-color: var(--canvas-bg);
    }
    
    .stApp {
        background-color: var(--canvas-bg);
    }

    /* ========================================================
       SUPER ELEGANT SIDEBAR (WARM NOIR & CHAMPAGNE ACCENTS)
       ======================================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #140E0C 0%, #1A1310 50%, #231915 100%) !important;
        border-right: 1px solid rgba(197, 160, 89, 0.22) !important;
        box-shadow: 6px 0 30px rgba(0, 0, 0, 0.18) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #EAE0D6 !important;
    }

    section[data-testid="stSidebar"] label {
        font-size: 10.5px !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        color: #C5A059 !important;
        margin-bottom: 6px !important;
    }

    /* Style selectboxes and inputs inside sidebar */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(197, 160, 89, 0.32) !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FAF7F2 !important;
        font-size: 13px !important;
    }

    .sidebar-brand-block {
        padding: 6px 4px 18px 4px;
        border-bottom: 1px solid rgba(197, 160, 89, 0.22);
        margin-bottom: 22px;
    }

    .sidebar-crest {
        font-size: 26px;
        line-height: 1;
        margin-bottom: 6px;
        color: #C5A059;
    }

    .sidebar-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 0.06em;
        color: #FAF7F2;
        margin: 0;
    }

    .sidebar-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 9px;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #C5A059;
        margin-top: 4px;
        font-weight: 500;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(197, 160, 89, 0.2);
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 20px;
    }

    .sidebar-card-title {
        font-size: 10px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #C5A059;
        font-weight: 600;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .sidebar-stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        padding: 5px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .sidebar-stat-row:last-child {
        border-bottom: none;
    }

    .sidebar-stat-name {
        color: #D8CCC2;
        font-weight: 400;
    }

    .sidebar-stat-val {
        color: #FAF7F2;
        font-weight: 600;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .sidebar-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(197, 160, 89, 0.12);
        border: 1px solid rgba(197, 160, 89, 0.35);
        color: #E2CA96;
        font-size: 10px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        margin-top: 8px;
    }

    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #C5A059;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #C5A059;
    }

    /* ========================================================
       EDITORIAL HERO SECTION
       ======================================================== */
    .hero-container {
        background: linear-gradient(135deg, #15100E 0%, #221A16 55%, #30231D 100%);
        border-radius: 16px;
        padding: 46px 46px 40px 46px;
        margin-bottom: 28px;
        color: #FAF7F2;
        position: relative;
        box-shadow: 0 24px 48px rgba(21, 16, 14, 0.12);
        border: 1px solid rgba(197, 160, 89, 0.28);
    }
    
    .hero-eyebrow {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        color: #C5A059;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .hero-eyebrow::before {
        content: "";
        width: 22px;
        height: 1px;
        background-color: #C5A059;
        display: inline-block;
    }

    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 42px;
        line-height: 1.14;
        font-weight: 400;
        letter-spacing: -0.02em;
        color: #FAF7F2;
        margin-bottom: 14px;
    }

    .hero-title em {
        font-style: italic;
        font-family: 'Playfair Display', serif;
        color: #E2CA96;
        font-weight: 400;
    }

    .hero-desc {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        line-height: 1.65;
        color: #D6CBC2;
        max-width: 660px;
        font-weight: 300;
    }

    /* Executive KPI Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 28px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #EAE2D7;
        border-radius: 12px;
        padding: 22px 20px;
        box-shadow: 0 4px 16px rgba(34, 26, 22, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(34, 26, 22, 0.07);
        border-color: #C5A059;
    }

    .metric-label {
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #84756A;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        font-weight: 600;
        color: #1F1815;
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .metric-badge {
        font-size: 11px;
        font-weight: 500;
        color: #A67C48;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    /* Luxury Tags & Badges */
    .tag-sms {
        background-color: #F1ECE6;
        color: #4D4037;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #DFD5CA;
        display: inline-block;
    }

    .tag-call {
        background-color: #FDF4E7;
        color: #8F6219;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #F0D7AE;
        display: inline-block;
    }

    .tag-visit {
        background-color: #FBF0ED;
        color: #9C3826;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #ECCDC6;
        display: inline-block;
    }

    .tag-vulnerable {
        background-color: #F7EFE2;
        color: #8D5B18;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #E6D0AC;
        display: inline-block;
    }

    /* Dossier Card View */
    .dossier-card {
        background: #FFFFFF;
        border: 1px solid #EAE2D7;
        border-radius: 14px;
        padding: 28px;
        margin-top: 16px;
        box-shadow: 0 8px 32px rgba(34, 26, 22, 0.04);
        position: relative;
    }

    .dossier-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 32px;
        right: 32px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #C5A059, transparent);
    }

    .dossier-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        border-bottom: 1px solid #F2ECE4;
        padding-bottom: 16px;
        margin-bottom: 20px;
    }

    .dossier-id {
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        color: #1F1815;
    }

    .dossier-meta {
        font-size: 11.5px;
        color: #84756A;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* Probability Visual Meter */
    .prob-meter-wrapper {
        background: #F1ECE6;
        border-radius: 10px;
        height: 8px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
    }

    .prob-meter-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #A67C48 0%, #C5A059 100%);
    }

    /* Refined Streamlit Native Overrides */
    div[data-baseweb="tab-list"] {
        border-bottom: 1px solid #E8DFD4 !important;
        gap: 28px !important;
    }

    button[data-baseweb="tab"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 17px !important;
        color: #84756A !important;
        background-color: transparent !important;
        border: none !important;
        padding: 12px 4px !important;
    }

    button[aria-selected="true"] {
        color: #15100E !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #C5A059 !important;
    }

    .stDownloadButton button {
        background-color: #1A1310 !important;
        color: #FAF7F2 !important;
        border: 1px solid #C5A059 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 8px 18px !important;
        font-size: 13px !important;
        letter-spacing: 0.05em !important;
        transition: all 0.2s ease !important;
    }

    .stDownloadButton button:hover {
        background-color: #2D221D !important;
        border-color: #E2CA96 !important;
        color: #E2CA96 !important;
        transform: translateY(-1px) !important;
    }
</style>
"""), unsafe_allow_html=True)

if df_raw.empty:
    st.error("Weekly portfolio data not found. Please run `python run_pipeline.py` first.")
    st.stop()

# =============================================================
# SUPER ELEGANT SIDEBAR (10/10 EXECUTIVE TELEMETRY)
# =============================================================
with st.sidebar:
    st.markdown(textwrap.dedent("""
    <div class="sidebar-brand-block">
        <div class="sidebar-crest">⚜️</div>
        <h2 class="sidebar-title">SKYE8 PRIORITISER</h2>
        <div class="sidebar-subtitle">Haute Collections Intelligence &bull; Bamenda</div>
        <div class="sidebar-status-pill">
            <span class="pulse-dot"></span>
            Production Calibrated &bull; Zero Leakage
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    st.markdown("### 🎛️ Portfolio Controls")
    
    officers = ["All Collections Officers"] + sorted(df_raw["assigned_officer"].unique().tolist())
    selected_officer = st.selectbox("Assignee Filter", officers)

    channels = ["All Outreach Channels"] + sorted(df_raw["recommended_channel"].unique().tolist())
    selected_channel = st.selectbox("Outreach Channel", channels)

    vulnerability_filter = st.selectbox(
        "Ethical Safeguard Filter",
        ["All Accounts", "Standard Accounts Only", "Senior & Vulnerable Protected Only"]
    )

    min_prob = st.slider("Minimum Cure Probability", 0.0, 1.0, 0.0, 0.05)

    # Search Bar inside Sidebar
    search_query = st.text_input("🔍 Search Account or Loan Ref", placeholder="e.g. 103380")

    st.markdown("---")
    
    # Live Officer Caseload Card
    st.markdown(textwrap.dedent("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">👥 Officer Caseload Distribution</div>
    """), unsafe_allow_html=True)
    
    officer_counts = df_raw["assigned_officer"].value_counts()
    for off_name in sorted(officer_counts.index):
        cnt = officer_counts[off_name]
        short_name = off_name.split(" - ")[-1]
        st.markdown(textwrap.dedent(f"""
        <div class="sidebar-stat-row">
            <span class="sidebar-stat-name">{short_name}</span>
            <span class="sidebar-stat-val">{cnt} accounts</span>
        </div>
        """), unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Channel Cost Reference Card
    st.markdown(textwrap.dedent("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">💰 Channel Unit Economics</div>
        <div class="sidebar-stat-row">
            <span class="sidebar-stat-name">SMS Automated</span>
            <span class="sidebar-stat-val">50 FCFA</span>
        </div>
        <div class="sidebar-stat-row">
            <span class="sidebar-stat-name">Phone Negotiation</span>
            <span class="sidebar-stat-val">500 FCFA</span>
        </div>
        <div class="sidebar-stat-row">
            <span class="sidebar-stat-name">In-Person Field Visit</span>
            <span class="sidebar-stat-val">5,000 FCFA</span>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    # 1-Click Offline Export in Sidebar
    st.markdown("### 📥 Field Mobility")
    csv_buffer = io.StringIO()
    df_raw.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Full Call Sheet (CSV)",
        data=csv_buffer.getvalue(),
        file_name="Skye8_Weekly_Call_Sheet_Bamenda.csv",
        mime="text/csv",
        help="Download offline roster for field visits in Mezam division."
    )
    
    st.markdown(textwrap.dedent("""
    <div style="font-size: 10px; color: #84756A; text-align: center; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 18px;">
        Skye8 Final Project SKY8-DS-FP-005<br>Nahbila Faith &bull; October 2026
    </div>
    """), unsafe_allow_html=True)

# -------------------------------------------------------------
# FILTER DATA ENGINE
# -------------------------------------------------------------
df_filtered = df_raw.copy()

if selected_officer != "All Collections Officers":
    df_filtered = df_filtered[df_filtered["assigned_officer"] == selected_officer]

if selected_channel != "All Outreach Channels":
    df_filtered = df_filtered[df_filtered["recommended_channel"] == selected_channel]

if vulnerability_filter == "Standard Accounts Only":
    df_filtered = df_filtered[~df_filtered["is_vulnerable"]]
elif vulnerability_filter == "Senior & Vulnerable Protected Only":
    df_filtered = df_filtered[df_filtered["is_vulnerable"]]

df_filtered = df_filtered[df_filtered["recovery_probability"] >= min_prob]

if search_query:
    q = search_query.strip().lower()
    df_filtered = df_filtered[
        df_filtered["SK_ID_CURR"].astype(str).str.contains(q) |
        df_filtered["SK_ID_PREV"].astype(str).str.contains(q)
    ]

# -------------------------------------------------------------
# HERO BANNER (EDITORIAL LUXURY DESIGN)
# -------------------------------------------------------------
st.markdown(textwrap.dedent("""
<div class="hero-container">
    <div class="hero-eyebrow">Skye8 Intelligence &bull; Core ML &bull; Bamenda, Cameroon</div>
    <div class="hero-title">The <em>precision</em> of recovery,<br>the <em>depth</em> of care.</div>
    <div class="hero-desc">
        A predictive decision engine ranking the arrears portfolio by expected recovery value,
        optimizing contact channel economics, and safeguarding vulnerable borrowers across 400 credit union accounts.
    </div>
</div>
"""), unsafe_allow_html=True)

# -------------------------------------------------------------
# EXECUTIVE KPI METRICS (BESPOKE MASTERPIECE GRID)
# -------------------------------------------------------------
total_overdue = df_filtered["overdue_amount"].sum()
expected_rec = df_filtered["expected_gross_recovery_fcfa"].sum()
total_cost = df_filtered["channel_cost_fcfa"].sum()
net_rec = expected_rec - total_cost

st.markdown(textwrap.dedent(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Active Arrears Book</div>
        <div class="metric-value">{total_overdue:,.0f} <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#84756A;">FCFA</span></div>
        <div class="metric-badge">{len(df_filtered)} Active Accounts</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Expected Recovery</div>
        <div class="metric-value">{expected_rec:,.0f} <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#84756A;">FCFA</span></div>
        <div class="metric-badge">{expected_rec/max(1.0, total_overdue):.1%} of Delinquent Balance</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Action Cost & Net</div>
        <div class="metric-value">{net_rec:,.0f} <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#84756A;">FCFA</span></div>
        <div class="metric-badge">Outreach Cost: {total_cost:,.0f} FCFA</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Precision @ 100 Accounts</div>
        <div class="metric-value">87.0%</div>
        <div class="metric-badge">12.4x vs Incumbent Heuristic (7.0%)</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Net Financial Lift</div>
        <div class="metric-value">+2,112,657 <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#84756A;">FCFA</span></div>
        <div class="metric-badge">+64.0% Added Cash per 100 Accounts</div>
    </div>
</div>
"""), unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN EDITORIAL TABS
# -------------------------------------------------------------
tab_dossier, tab_table, tab_financials, tab_ethics = st.tabs([
    "Dossier Inspector",
    "Prioritised Call Book",
    "Financial & ML Validation",
    "Ethical Safeguards"
])

# TAB 1: BESPOKE DOSSIER INSPECTOR (10/10 MASTERPIECE)
with tab_dossier:
    st.markdown("### Client Dossier & Actionable Guidance")
    st.caption("Select a borrower account to inspect their historical payment trajectory, recovery probability meter, and field contact script.")
    
    selected_account = st.selectbox(
        "Select Account Number",
        df_filtered["SK_ID_CURR"].tolist() if not df_filtered.empty else []
    )
    
    if selected_account:
        acc = df_filtered[df_filtered["SK_ID_CURR"] == selected_account].iloc[0]
        
        channel_tag_class = "tag-sms" if acc["recommended_channel"] == "SMS" else ("tag-call" if acc["recommended_channel"] == "CALL" else "tag-visit")
        vulnerable_tag = f'<span class="tag-vulnerable">Protected &bull; Senior / Hardship</span>' if acc["is_vulnerable"] else '<span class="tag-sms">Standard Operational Flow</span>'
        
        # Script tone guidance
        script_tone = "Acknowledge customer loyalty, verify hardship context, and offer flexible 14-day instalment restructuring." if acc['is_vulnerable'] else "Polite notification of 15-day arrears mark; confirm commitment to settle within 30-day grace cycle."
        prob_pct = acc['recovery_probability'] * 100.0

        # Dedicated Flush-Left HTML Card: zero leading spaces guarantees clean markdown rendering
        dossier_html = f"""<div class="dossier-card">
<div class="dossier-header">
<div>
<span class="dossier-meta">Borrower Account Reference</span>
<div class="dossier-id">Client #{acc['SK_ID_CURR']} &bull; Loan Ref {acc['SK_ID_PREV']}</div>
</div>
<div>
<span class="{channel_tag_class}">Recommended Action: {acc['recommended_channel']}</span>
&nbsp;
{vulnerable_tag}
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 24px;">
<div>
<div class="metric-label">Overdue Balance</div>
<div style="font-size: 20px; font-weight: 600; color: #1F1815;">{acc['overdue_amount']:,.0f} FCFA</div>
<div style="font-size: 11px; color: #84756A;">15 Days Past Due</div>
</div>
<div>
<div class="metric-label">Recovery Probability</div>
<div style="font-size: 20px; font-weight: 600; color: #C5A059;">{acc['recovery_probability']:.1%}</div>
<div class="prob-meter-wrapper"><div class="prob-meter-fill" style="width: {prob_pct:.1f}%;"></div></div>
<div style="font-size: 11px; color: #84756A; margin-top: 4px;">Calibrated ML Estimate</div>
</div>
<div>
<div class="metric-label">Assigned Officer</div>
<div style="font-size: 18px; font-weight: 600; color: #1F1815;">{acc['assigned_officer']}</div>
<div style="font-size: 11px; color: #84756A;">Mezam / Bamenda Unit</div>
</div>
<div>
<div class="metric-label">Net Yield Expectation</div>
<div style="font-size: 20px; font-weight: 600; color: #2E5A36;">{acc['expected_net_recovery_fcfa']:,.0f} FCFA</div>
<div style="font-size: 11px; color: #84756A;">Net of Action Cost ({acc['channel_cost_fcfa']:,.0f} FCFA)</div>
</div>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; padding-top: 16px; border-top: 1px solid #F0EAE2;">
<div>
<div class="metric-label">Behavioral Track Record (Pre-Arrears)</div>
<ul style="font-size: 13px; color: #4A3E36; line-height: 1.8; margin-top: 6px; padding-left: 18px;">
<li>Prior Instalment Count: <strong>{int(acc['prior_instalments_count'])} scheduled payments</strong></li>
<li>Historical Delinquency Rate: <strong>{acc['prior_late_ratio']:.1%} of past instalments</strong></li>
<li>Past Severe Delinquencies (15+ days): <strong>{int(acc['prior_severe_late_count'])}</strong></li>
<li>Average Historical Delay: <strong>{acc['prior_avg_days_late']:.1f} days</strong></li>
<li>Repayment Compliance Ratio: <strong>{acc['prior_payment_ratio']:.1%}</strong></li>
</ul>
</div>
<div>
<div class="metric-label">Officer Engagement Rationale & Script</div>
<div style="background-color: #FAF7F2; border: 1px solid #EAE2D7; border-radius: 8px; padding: 14px; margin-top: 6px;">
<div style="font-size: 13px; font-weight: 600; color: #1F1815; margin-bottom: 4px;">Strategic Reasoning:</div>
<div style="font-size: 12.5px; color: #5C5047; line-height: 1.5; margin-bottom: 10px;">{acc['action_reason']}</div>
<div style="font-size: 13px; font-weight: 600; color: #1F1815; margin-bottom: 4px;">Recommended Dialogue Tone:</div>
<div style="font-size: 12.5px; color: #5C5047; font-style: italic;">
"{script_tone}"
</div>
</div>
</div>
</div>
</div>"""
        st.markdown(dossier_html, unsafe_allow_html=True)

# TAB 2: PRIORITISED TABLE VIEW
with tab_table:
    st.markdown("### Weekly Prioritised Call Book (400 Accounts)")
    st.caption("Ordered by Expected Recoverable Cash Flow (P(recovery) × Debt). Prioritizing high-probability, high-yield accounts first.")
    
    # Officer-specific download button
    sub_col1, sub_col2 = st.columns([3, 1])
    with sub_col2:
        officer_buf = io.StringIO()
        df_filtered.to_csv(officer_buf, index=False)
        st.download_button(
            label=f"📥 Export Current View ({len(df_filtered)} Rows)",
            data=officer_buf.getvalue(),
            file_name="Prioritised_Call_Roster.csv",
            mime="text/csv"
        )
    
    display_df = df_filtered[[
        "rank", "SK_ID_CURR", "assigned_officer", "overdue_amount",
        "recovery_probability", "recommended_channel", "channel_cost_fcfa",
        "expected_gross_recovery_fcfa", "is_vulnerable", "action_reason"
    ]].copy()
    
    display_df = display_df.rename(columns={
        "rank": "Rank",
        "SK_ID_CURR": "Borrower ID",
        "assigned_officer": "Officer",
        "overdue_amount": "Overdue (FCFA)",
        "recovery_probability": "Cure Prob",
        "recommended_channel": "Channel",
        "channel_cost_fcfa": "Cost (FCFA)",
        "expected_gross_recovery_fcfa": "Expected Yield (FCFA)",
        "is_vulnerable": "Protected",
        "action_reason": "Rationale"
    })
    
    st.dataframe(
        display_df.style.format({
            "Overdue (FCFA)": "{:,.0f}",
            "Cure Prob": "{:.1%}",
            "Cost (FCFA)": "{:,.0f}",
            "Expected Yield (FCFA)": "{:,.0f}",
            "Protected": lambda x: "🛡️ Protected" if x else "Standard"
        }),
        height=500
    )

# TAB 3: FINANCIAL & ML VALIDATION
with tab_financials:
    st.markdown("### Quantitative Proof: Numbers, Not Adjectives")
    st.caption("Rigorous evaluation on 9,219 unseen arrears accounts on the held-out test partition.")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("#### Precision Comparison (Accounts Cured / Contacts Made)")
        st.markdown("Matching the operational capacity of 3 collections officers in Bamenda:")
        
        prec_table = pd.DataFrame({
            "Policy Strategy": [
                "Skye8 AI Prioritiser (Expected Value)",
                "Incumbent Heuristic (Biggest Debt First)",
                "Random / Unassisted Baseline"
            ],
            "Top 50 Accounts (1-2 Weeks)": ["90.00%", "14.00%", "18.00%"],
            "Top 100 Accounts (Full Month)": ["87.00%", "7.00%", "17.00%"],
            "Relative Precision Lift": ["12.43x Higher", "1.00x (Baseline)", "2.42x"]
        })
        st.table(prec_table)
        
    with col_t2:
        st.markdown("#### Cash Collected Comparison (Francs CFA)")
        st.markdown("Actual money recovered from delinquent portfolios:")
        
        cash_table = pd.DataFrame({
            "Policy Strategy": [
                "Skye8 AI Prioritiser (Expected Value)",
                "Incumbent Heuristic (Biggest Debt First)",
                "Net Financial Gain (Lift in FCFA)"
            ],
            "Top 50 Accounts": ["4,529,712 FCFA", "3,301,388 FCFA", "+1,228,324 FCFA (+37.2%)"],
            "Top 100 Accounts": ["5,414,045 FCFA", "3,301,388 FCFA", "+2,112,657 FCFA (+64.0%)"]
        })
        st.table(cash_table)

    st.markdown(textwrap.dedent("""
    <div style="background-color: #FFFFFF; border-left: 3px solid #C5A059; border-radius: 8px; padding: 18px; margin-top: 16px; border: 1px solid #EAE2D7;">
        <strong style="color: #1F1815; font-family: 'Playfair Display', serif; font-size: 16px;">Why 'Biggest Debt First' Loses Money:</strong>
        <p style="font-size: 13.5px; color: #5C5047; margin-top: 6px; line-height: 1.6;">
            Sorting purely by debt size directs collections officers to accounts with massive overdue balances that have an 86%–93% failure rate.
            These accounts have suffered fatal business distress or displacement.
            By conditioning rankings on <strong>Expected Recoverable Value</strong> ($P(\text{cure}) \times \text{Debt}$),
            officers engage borrowers with substantial debts who retain active capacity and willingness to settle,
            recovering an additional <strong>2,112,657 FCFA per 100 worked accounts</strong>.
        </p>
    </div>
    """), unsafe_allow_html=True)

# TAB 4: ETHICAL SAFEGUARDS
with tab_ethics:
    st.markdown("### Ethical Guardrails & The Human Cost")
    st.caption("Protecting vulnerable borrowers and preserving community trust in the North West Region of Cameroon.")
    
    eth_col1, eth_col2 = st.columns([1.5, 1])
    
    with eth_col1:
        st.markdown(textwrap.dedent("""
        #### The Reality of Debt in Bamenda
        Microfinance borrowers are market traders, school teachers, smallholders, and artisans.
        They face severe exogenous disruptions:
        * Regional economic headwinds and transport bottlenecks.
        * Health emergencies and funeral contributions.
        * Supply-chain inventory losses.
        
        A naive collections tool that maximizes pressure pushes officers toward aggressive harassment,
        destroying the MFI's social license and driving borrowers into deeper insolvency.
        
        #### Embedded Technological Protections:
        1. **Senior Hardship Shield:** Borrowers aged >= 60 years are automatically shielded from high-pressure contacts and routed to cooperative welfare restructuring.
        2. **Employment Shock Flag:** Documented income disruptions trigger loan restructuring proposals rather than field enforcement.
        3. **Cost-Gated In-Person Enforcement:** Field visits (5,000 FCFA) are prohibited on low balances and vulnerable borrowers.
        """))
        
    with eth_col2:
        st.markdown("#### Active Welfare Audit (400 Accounts)")
        st.markdown(textwrap.dedent("""
        <div style="background: #FFFFFF; border: 1px solid #EAE2D7; border-radius: 12px; padding: 20px;">
            <div style="font-size: 32px; font-family: 'Playfair Display', serif; color: #8D5B18; font-weight: 600;">74 Borrowers</div>
            <div style="font-size: 12px; color: #84756A; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">Protected by Ethical Filters (18.5%)</div>
            <div style="font-size: 12.5px; color: #5C5047; line-height: 1.6;">
                These accounts have been diverted from aggressive visits to friendly restructuring dialogues.
                Overdue balances are preserved without inflicting humanitarian harm on distressed families.
            </div>
        </div>
        """), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(textwrap.dedent("""
<div style="display: flex; justify-content: space-between; font-size: 11px; color: #84756A; letter-spacing: 0.08em; text-transform: uppercase;">
    <div>Skye8 Company Ltd &bull; Final Project SKY8-DS-FP-005</div>
    <div>Candidate: Nahbila Faith &bull; Bamenda, Cameroon</div>
</div>
"""), unsafe_allow_html=True)
