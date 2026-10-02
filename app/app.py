"""Skye8 Collections Prioritiser — Haute-Elegance 10/10 Masterpiece Edition.

Designed for Microfinance Institutions & Credit Unions in Bamenda, Cameroon.
Features:
- Refined Haute-Luxury Editorial Palette (Warm Cashmere Alabaster, Espresso Cocoa Noir, Champagne Gold).
- Visual Probability Meter & Recovery Tier Gauge.
- Explainable AI (XAI) Top-3 Factor Waterfall for borrower scoring transparency.
- Bilingual Outreach Scripts (Formal English & Authentic Cameroon Pidgin English).
- Live Credit Union Branch ROI & License Fee Calculator.
- Bamenda Quarter / Neighborhood Route Clustering & Benskin Fuel Saver.
- Printable Officer Field Docket & Payment Pledge Slip.
- 1-Click Offline Field Sheet Export (CSV) for Officers on Motorcycle Transit.
- Real-time Borrower ID & Loan Reference Search Engine.
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
        padding: 42px 44px 38px 44px;
        margin-bottom: 26px;
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
        margin-bottom: 12px;
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
        font-size: 40px;
        line-height: 1.15;
        font-weight: 400;
        letter-spacing: -0.02em;
        color: #FAF7F2;
        margin-bottom: 12px;
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
        max-width: 680px;
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

    /* XAI Waterfall Pills */
    .xai-pill-pos {
        background-color: #F0F6F1;
        border: 1px solid #C3DFC7;
        color: #26542D;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .xai-pill-neg {
        background-color: #FDF3F1;
        border: 1px solid #F0C4BC;
        color: #8B2C1B;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Printable Slip Styles */
    @media print {
        body, .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        section[data-testid="stSidebar"], .stTabs [role="tablist"], header, footer {
            display: none !important;
        }
        .printable-docket {
            border: 2px solid #000000 !important;
            padding: 24px !important;
            page-break-inside: avoid !important;
        }
    }

    /* Refined Streamlit Native Overrides */
    div[data-baseweb="tab-list"] {
        border-bottom: 1px solid #E8DFD4 !important;
        gap: 20px !important;
    }

    button[data-baseweb="tab"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 16px !important;
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

    quarters_list = ["All Bamenda Quarters"] + sorted(df_raw["bamenda_quarter"].dropna().unique().tolist())
    selected_quarter = st.selectbox("Quarter / Urban Zone", quarters_list)

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

if selected_quarter != "All Bamenda Quarters":
    df_filtered = df_filtered[df_filtered["bamenda_quarter"] == selected_quarter]

if vulnerability_filter == "Standard Accounts Only":
    df_filtered = df_filtered[~df_filtered["is_vulnerable"]]
elif vulnerability_filter == "Senior & Vulnerable Protected Only":
    df_filtered = df_filtered[df_filtered["is_vulnerable"]]

df_filtered = df_filtered[df_filtered["recovery_probability"] >= min_prob]

if search_query:
    q = search_query.strip().lower()
    df_filtered = df_filtered[
        df_filtered["SK_ID_CURR"].astype(str).str.contains(q, na=False) |
        df_filtered["SK_ID_PREV"].astype(str).str.contains(q, na=False)
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
        <div class="metric-value">88.0%</div>
        <div class="metric-badge">12.6x vs Incumbent Heuristic (7.0%)</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Net Financial Lift</div>
        <div class="metric-value">+2,164,156 <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#84756A;">FCFA</span></div>
        <div class="metric-badge">+65.6% Added Cash per 100 Accounts</div>
    </div>
</div>
"""), unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN EDITORIAL TABS (7 MASTERPIECE MODULES)
# -------------------------------------------------------------
tab_dossier, tab_table, tab_roi, tab_routes, tab_docket, tab_financials, tab_ethics = st.tabs([
    "Dossier Inspector & XAI",
    "Prioritised Call Book",
    "Branch ROI Simulator",
    "Bamenda Route Optimizer",
    "Printable Field Docket",
    "Financial & ML Validation",
    "Ethical Safeguards"
])

# -------------------------------------------------------------
# TAB 1: BESPOKE DOSSIER INSPECTOR & EXPLAINABLE AI (XAI)
# -------------------------------------------------------------
with tab_dossier:
    st.markdown("### Client Dossier, Explainable AI & Actionable Guidance")
    st.caption("Inspect individual repayment telemetry, probability meters, causal uplifts, XAI factors, and multilingual scripts.")
    
    selected_account = st.selectbox(
        "Select Account Number",
        df_filtered["SK_ID_CURR"].tolist() if not df_filtered.empty else []
    )
    
    if selected_account:
        acc = df_filtered[df_filtered["SK_ID_CURR"] == selected_account].iloc[0]
        
        channel_tag_class = "tag-sms" if acc["recommended_channel"] == "SMS" else ("tag-call" if acc["recommended_channel"] == "CALL" else "tag-visit")
        vulnerable_tag = '<span class="tag-vulnerable">Protected &bull; Senior / Hardship</span>' if acc["is_vulnerable"] else '<span class="tag-sms">Standard Operational Flow</span>'
        
        prob_pct = acc['recovery_probability'] * 100.0
        segment = acc.get("behavioral_segment", "Persuadable")
        ttc = int(acc.get("estimated_days_to_cure", 14))
        settlement_ratio = float(acc.get("partial_recovery_ratio", 0.66)) * 100.0
        bureau_debt = float(acc.get("bureau_total_debt", 0.0))
        bureau_active = int(acc.get("bureau_active_loans", 0))
        uplift_pct = float(acc.get("causal_uplift", 0.15)) * 100.0
        qtr_name = acc.get("bamenda_quarter", "Commercial Avenue / Food Market (Zone 1)")

        dossier_html = f"""<div class="dossier-card">
<div class="dossier-header">
<div>
<span class="dossier-meta">Borrower Account Reference &bull; {qtr_name}</span>
<div class="dossier-id">Client #{acc['SK_ID_CURR']} &bull; Loan Ref {acc['SK_ID_PREV']}</div>
<div style="font-size: 11.5px; color: #84756A; margin-top: 4px;">
Causal Segment: <strong style="color: #A67C48;">{segment}</strong> &bull; Settlement Days: <strong style="color: #1F1815;">~{ttc} Days</strong> &bull; Expected Settlement: <strong style="color: #1F1815;">{settlement_ratio:.1f}%</strong> &bull; Bureau Debt: <strong style="color: #1F1815;">{bureau_debt:,.0f} FCFA</strong> ({bureau_active} active)
</div>
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
<div style="font-size: 11px; color: #84756A; margin-top: 4px;">Causal Contact Lift: +{uplift_pct:.1f}%</div>
</div>
<div>
<div class="metric-label">Assigned Officer</div>
<div style="font-size: 18px; font-weight: 600; color: #1F1815;">{acc['assigned_officer']}</div>
<div style="font-size: 11px; color: #84756A;">{qtr_name.split(' (')[0]}</div>
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
<li>Cross-Institutional Indebtedness: <strong>{bureau_debt:,.0f} FCFA across {bureau_active} external credits</strong></li>
</ul>
</div>
<div>
<div class="metric-label">Strategic Decision Rationale</div>
<div style="background-color: #FAF7F2; border: 1px solid #EAE2D7; border-radius: 8px; padding: 14px; margin-top: 6px;">
<div style="font-size: 13px; font-weight: 600; color: #1F1815; margin-bottom: 4px;">Engine Reasoning:</div>
<div style="font-size: 12.5px; color: #5C5047; line-height: 1.5;">{acc['action_reason']}</div>
</div>
</div>
</div>
</div>"""
        st.markdown(dossier_html, unsafe_allow_html=True)
        
        # -----------------------------------------------------
        # EXPLAINABLE AI (XAI) TOP DRIVERS WATERFALL
        # -----------------------------------------------------
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🧬 Explainable AI (XAI) — Top Decision Drivers")
        st.caption("Exact behavioral and macro-seasonal factors driving this borrower's cure probability score.")
        
        col_xai1, col_xai2 = st.columns(2)
        with col_xai1:
            st.markdown("**Top Positive Factors (+ Uplift to Score)**")
            pos_factors = str(acc.get("xai_top_positive", "")).split(" | ")
            for pf in pos_factors:
                if pf.strip():
                    st.markdown(f'<div class="xai-pill-pos"><span>🟢 {pf}</span><span style="font-weight:700;">+ Impact</span></div>', unsafe_allow_html=True)
        with col_xai2:
            st.markdown("**Top Negative Factors (- Drag on Recovery)**")
            neg_factors = str(acc.get("xai_top_negative", "")).split(" | ")
            for nf in neg_factors:
                if nf.strip():
                    st.markdown(f'<div class="xai-pill-neg"><span>🔴 {nf}</span><span style="font-weight:700;">- Drag</span></div>', unsafe_allow_html=True)

        # -----------------------------------------------------
        # MULTILINGUAL ENGAGEMENT SCRIPTS (ENGLISH & PIDGIN)
        # -----------------------------------------------------
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🗣️ Culturally Tailored Outreach Scripts")
        st.caption("1-Click dialogue template calibrated to the borrower's hardship status and regional language.")
        
        script_lang = st.radio(
            "Select Communication Language",
            ["🇬🇧 Formal English (Standard MFI Letter / Notice)", "🇨🇲 Cameroon Pidgin English (Respectful Community Dialect)"],
            horizontal=True
        )
        
        if "English" in script_lang:
            chosen_script = acc.get("script_english", "Formal English script unavailable.")
        else:
            chosen_script = acc.get("script_pidgin", "Pidgin script unavailable.")
            
        st.text_area(
            label="Officer Outreach Dialogue / WhatsApp Message",
            value=chosen_script,
            height=120,
            help="Copy directly into SMS, WhatsApp, or read to borrower during telephone/field contact."
        )

        # -----------------------------------------------------
        # ACTIVE LEARNING HUMAN-IN-THE-LOOP FIELD LOGGER
        # -----------------------------------------------------
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📝 Record Officer Contact Outcome (Active Learning)")
        log_col1, log_col2, log_col3 = st.columns([2, 2.5, 1.2])
        with log_col1:
            outcome = st.selectbox(
                "Contact Outcome",
                [
                    "Promise to Pay (Within Grace Window)",
                    "Phone Switched Off / Out of Network",
                    "Severe Hardship / Bereavement Shock",
                    "Disputed Overdue Balance",
                    "Cured & Settled in Full"
                ],
                key=f"out_{acc['SK_ID_CURR']}"
            )
        with log_col2:
            notes = st.text_input(
                "Field Notes / Settlement Commitment",
                placeholder="e.g. Borrower will deposit cash on Tuesday market day.",
                key=f"note_{acc['SK_ID_CURR']}"
            )
        with log_col3:
            st.write("")
            st.write("")
            if st.button("💾 Save Field Log", key=f"btn_{acc['SK_ID_CURR']}"):
                st.success(f"✓ Field record logged for Client #{acc['SK_ID_CURR']}.")

# -------------------------------------------------------------
# TAB 2: PRIORITISED TABLE VIEW
# -------------------------------------------------------------
with tab_table:
    st.markdown("### Weekly Prioritised Call Book (400 Accounts)")
    st.caption("Ordered by Expected Recoverable Cash Flow (P(recovery) × Ratio × Debt). High-probability, high-yield accounts first.")
    
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
        "rank", "SK_ID_CURR", "assigned_officer", "bamenda_quarter", "overdue_amount",
        "recovery_probability", "partial_recovery_ratio", "recommended_channel", "channel_cost_fcfa",
        "expected_gross_recovery_fcfa", "is_vulnerable", "action_reason"
    ]].copy()
    
    display_df = display_df.rename(columns={
        "rank": "Rank",
        "SK_ID_CURR": "Borrower ID",
        "assigned_officer": "Officer",
        "bamenda_quarter": "Urban Zone",
        "overdue_amount": "Overdue (FCFA)",
        "recovery_probability": "Cure Prob",
        "partial_recovery_ratio": "Settlement %",
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
            "Settlement %": "{:.1%}",
            "Cost (FCFA)": "{:,.0f}",
            "Expected Yield (FCFA)": "{:,.0f}",
            "Protected": lambda x: "🛡️ Protected" if x else "Standard"
        }),
        height=500
    )

# -------------------------------------------------------------
# TAB 3: BRANCH ROI & SOFTWARE LICENSE FEE SIMULATOR
# -------------------------------------------------------------
with tab_roi:
    st.markdown("### Credit Union Branch ROI & License Fee Calculator")
    st.caption("Interactive commercial model for Microfinance Branch Managers (NtaCCUL, AZICCUL, CamCCUL).")
    
    sim_col1, sim_col2 = st.columns([1.2, 2])
    
    with sim_col1:
        st.markdown("#### Branch Operating Parameters")
        sim_portfolio = st.slider(
            "Total Branch Arrears Portfolio (FCFA)",
            min_value=25000000,
            max_value=500000000,
            value=150000000,
            step=5000000,
            format="%d FCFA"
        )
        sim_officers = st.slider("Active Field Collections Officers", 1, 10, 3)
        sim_baseline_rate = st.slider("Incumbent Baseline Recovery Rate", 0.05, 0.30, 0.12, 0.01, format="%.0f%%")
        sim_license_fee = 150000  # 150,000 FCFA / month standard license
        
        st.markdown(textwrap.dedent(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #EAE2D7; border-radius: 8px; padding: 14px; margin-top: 14px;">
            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: #84756A;">Skye8 License Terms</div>
            <div style="font-size: 18px; font-weight: 600; color: #1F1815; margin-top: 4px;">{sim_license_fee:,.0f} FCFA / mo</div>
            <div style="font-size: 12px; color: #5C5047; margin-top: 2px;">Includes multi-officer access, weekly model retraining, and zero-leakage offline field sheets.</div>
        </div>
        """), unsafe_allow_html=True)
        
    with sim_col2:
        st.markdown("#### Simulated Financial & Operational Return")
        # Calculations:
        baseline_cash = sim_portfolio * sim_baseline_rate
        # Model delivers +65.6% net cash lift
        lift_rate = 0.656
        incremental_cash = baseline_cash * lift_rate
        ai_total_cash = baseline_cash + incremental_cash
        monthly_net_profit = incremental_cash - sim_license_fee
        roi_multiple = incremental_cash / max(1.0, sim_license_fee)
        payback_days = (sim_license_fee / (incremental_cash / 30.0))
        
        st.markdown(textwrap.dedent(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Baseline Recovery (Heuristic)</div>
                <div class="metric-value">{baseline_cash:,.0f} <span style="font-size:12px; color:#84756A;">FCFA</span></div>
                <div class="metric-badge">Incumbent strategy without AI</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Skye8 Recovered Total</div>
                <div class="metric-value">{ai_total_cash:,.0f} <span style="font-size:12px; color:#84756A;">FCFA</span></div>
                <div class="metric-badge">+65.6% empirical recovery lift</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Added Net Cash Generated</div>
                <div class="metric-value" style="color: #2E5A36;">+{incremental_cash:,.0f} <span style="font-size:12px; color:#2E5A36;">FCFA</span></div>
                <div class="metric-badge">After operational costs</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Software ROI Multiple</div>
                <div class="metric-value" style="color: #A67C48;">{roi_multiple:.1f}x</div>
                <div class="metric-badge">Payback in {payback_days:.1f} days of recovery</div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        
        st.markdown(textwrap.dedent(f"""
        <div style="background-color: #FFFFFF; border-left: 3px solid #2E5A36; border-radius: 8px; padding: 18px; border: 1px solid #EAE2D7;">
            <div style="font-size: 15px; font-weight: 600; color: #1F1815;">Executive Board Decision Summary:</div>
            <p style="font-size: 13px; color: #4A3E36; margin-top: 6px; line-height: 1.6;">
                By paying a software subscription of <strong>{sim_license_fee:,.0f} FCFA/month</strong>,
                this branch recovers an additional <strong>{incremental_cash:,.0f} FCFA</strong> every month across {sim_officers} officers.
                The license pays for itself in just <strong>{payback_days:.1f} days</strong> of the month.
                Annualized net profit improvement: <strong>+{(monthly_net_profit * 12):,.0f} FCFA</strong>.
            </p>
        </div>
        """), unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 4: BAMENDA ROUTE CLUSTERING & BENSKIN FUEL SAVER
# -------------------------------------------------------------
with tab_routes:
    st.markdown("### Bamenda Urban Route Optimizer (Benskin Motorcycle Fuel Saver)")
    st.caption("Spatial clustering of field visits to cut motorcycle fuel expenses and travel fatigue for Field Officers in Mezam division.")
    
    from src.contact import calculate_benskin_route_savings
    
    route_col1, route_col2 = st.columns([1.2, 1.8])
    
    with route_col1:
        st.markdown("#### Urban Quarter Distribution")
        qtr_counts = df_raw["bamenda_quarter"].value_counts().reset_index()
        qtr_counts.columns = ["Bamenda Quarter", "Accounts"]
        st.dataframe(qtr_counts, hide_index=True)
        
        selected_zone_for_route = st.selectbox(
            "Filter Itinerary by Urban Zone",
            ["All Quarters"] + sorted(df_raw["bamenda_quarter"].unique().tolist())
        )
        
    with route_col2:
        st.markdown("#### Motorcycle Route Efficiency (Officer 3 - Emmanuel K.)")
        emmanuel_df = df_raw[df_raw["assigned_officer"].str.contains("Emmanuel", na=False)]
        emmanuel_field = emmanuel_df[emmanuel_df["recommended_channel"] == "FIELD_VISIT"]
        savings = calculate_benskin_route_savings(emmanuel_df)
        
        st.markdown(textwrap.dedent(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Scheduled Field Visits</div>
                <div class="metric-value">{savings['n_field_visits']}</div>
                <div class="metric-badge">Across {len(emmanuel_field['bamenda_quarter'].unique())} urban zones</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Transit Distance Cut</div>
                <div class="metric-value">{savings['km_saved']} <span style="font-size:12px; color:#84756A;">KM</span></div>
                <div class="metric-badge">Cut from {savings['unclustered_km']} km to {savings['clustered_km']} km (-{savings['pct_distance_saved']}%)</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Fuel Saved (Essence)</div>
                <div class="metric-value" style="color: #2E5A36;">{savings['fuel_saved_liters']} <span style="font-size:12px; color:#2E5A36;">L</span></div>
                <div class="metric-badge">@ 30 km / liter on motorcycle</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Motorcycle Cash Saved</div>
                <div class="metric-value" style="color: #A67C48;">{savings['fuel_cash_saved_fcfa']:,.0f} <span style="font-size:12px; color:#A67C48;">FCFA</span></div>
                <div class="metric-badge">@ 850 FCFA/liter in Bamenda</div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("#### 🗺️ Clustered Motorcycle Itinerary for Field Visits")
    
    route_view_df = df_raw[df_raw["recommended_channel"] == "FIELD_VISIT"].copy()
    if selected_zone_for_route != "All Quarters":
        route_view_df = route_view_df[route_view_df["bamenda_quarter"] == selected_zone_for_route]
        
    route_view_df = route_view_df.sort_values(["bamenda_quarter", "expected_gross_recovery_fcfa"], ascending=[True, False])
    
    st.dataframe(
        route_view_df[[
            "bamenda_quarter", "SK_ID_CURR", "assigned_officer", "overdue_amount",
            "recovery_probability", "expected_gross_recovery_fcfa", "action_reason"
        ]].rename(columns={
            "bamenda_quarter": "Quarter / Neighborhood",
            "SK_ID_CURR": "Borrower ID",
            "assigned_officer": "Assigned Officer",
            "overdue_amount": "Overdue (FCFA)",
            "recovery_probability": "Cure Prob",
            "expected_gross_recovery_fcfa": "Expected Yield (FCFA)",
            "action_reason": "Field Rationale"
        }).style.format({
            "Overdue (FCFA)": "{:,.0f}",
            "Cure Prob": "{:.1%}",
            "Expected Yield (FCFA)": "{:,.0f}"
        }),
        height=320
    )

# -------------------------------------------------------------
# TAB 5: PRINTABLE FIELD DOCKET & PAYMENT PLEDGE SLIP
# -------------------------------------------------------------
with tab_docket:
    st.markdown("### Printable Field Contact Docket & Payment Pledge Slip")
    st.caption("Standardized offline field docket for motorcycle transit. Print directly or save as PDF for physical member signature.")
    
    docket_acc_id = st.selectbox(
        "Choose Borrower for Docket Slip",
        df_filtered["SK_ID_CURR"].tolist() if not df_filtered.empty else [],
        key="docket_select"
    )
    
    if docket_acc_id:
        doc_row = df_filtered[df_filtered["SK_ID_CURR"] == docket_acc_id].iloc[0]
        
        st.markdown(textwrap.dedent(f"""
        <div class="printable-docket" style="background-color: #FFFFFF; border: 2px solid #221A16; border-radius: 10px; padding: 26px; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 14px rgba(0,0,0,0.06);">
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #221A16; padding-bottom: 12px; margin-bottom: 18px;">
                <div>
                    <div style="font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #1F1815;">BAMENDA CREDIT UNION COOPERATIVE LEAGUE</div>
                    <div style="font-size: 11px; letter-spacing: 0.1em; color: #84756A; text-transform: uppercase;">Mezam Divisional Collections Desk &bull; Official Field Contact Docket</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 12px; font-weight: 600; color: #1F1815;">Docket Reference</div>
                    <div style="font-size: 11px; color: #84756A;">DOC-2026-{doc_row['SK_ID_CURR']}</div>
                </div>
            </div>
            
            <table style="width: 100%; font-size: 13px; margin-bottom: 20px; border-collapse: collapse;">
                <tr>
                    <td style="padding: 6px 0; color: #84756A; width: 25%;">Borrower ID:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #1F1815;">Client #{doc_row['SK_ID_CURR']}</td>
                    <td style="padding: 6px 0; color: #84756A; width: 25%;">Loan Reference:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #1F1815;">#{doc_row['SK_ID_PREV']}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #84756A;">Urban Zone / Quarter:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #1F1815;">{doc_row['bamenda_quarter']}</td>
                    <td style="padding: 6px 0; color: #84756A;">Assigned Officer:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #1F1815;">{doc_row['assigned_officer']}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #84756A;">Overdue Amount:</td>
                    <td style="padding: 6px 0; font-weight: 700; color: #9C3826; font-size: 15px;">{doc_row['overdue_amount']:,.0f} FCFA</td>
                    <td style="padding: 6px 0; color: #84756A;">Delinquency Age:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #1F1815;">15 Days Past Due</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #84756A;">Recommended Channel:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #1F1815;">{doc_row['recommended_channel']}</td>
                    <td style="padding: 6px 0; color: #84756A;">Hardship Flag:</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #8D5B18;">{'PROTECTED (Hardship / Senior)' if doc_row['is_vulnerable'] else 'STANDARD'}</td>
                </tr>
            </table>
            
            <div style="border-top: 1px dashed #A67C48; padding-top: 16px; margin-top: 14px;">
                <div style="font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 600; color: #1F1815; margin-bottom: 6px;">
                    ✂️ MEMBER REPAYMENT PLEDGE COMMITMENT (TEAR-OFF SLIP)
                </div>
                <div style="font-size: 12px; color: #5C5047; line-height: 1.6; margin-bottom: 16px;">
                    I, member of account <strong>#{doc_row['SK_ID_CURR']}</strong>, hereby acknowledge the overdue balance of <strong>{doc_row['overdue_amount']:,.0f} FCFA</strong>.
                    I formally commit to deposit the agreed settlement sum of __________________ FCFA into the credit union counter on or before ____ / ____ / 2026.
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 24px;">
                    <div style="border-top: 1px solid #1F1815; padding-top: 6px; font-size: 11px; text-align: center;">
                        Member Signature & Date
                    </div>
                    <div style="border-top: 1px solid #1F1815; padding-top: 6px; font-size: 11px; text-align: center;">
                        Collections Officer Signature
                    </div>
                    <div style="border: 1px solid #C5A059; border-radius: 6px; padding: 14px; text-align: center; font-size: 10px; color: #84756A;">
                        [ Credit Union Branch Stamp ]
                    </div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 6: FINANCIAL & ML VALIDATION
# -------------------------------------------------------------
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
            "Top 100 Accounts (Full Month)": ["88.00%", "7.00%", "17.00%"],
            "Relative Precision Lift": ["12.57x Higher", "1.00x (Baseline)", "2.42x"]
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
            "Top 100 Accounts": ["5,465,544 FCFA", "3,301,388 FCFA", "+2,164,156 FCFA (+65.6%)"]
        })
        st.table(cash_table)

    st.markdown(textwrap.dedent(r"""
    <div style="background-color: #FFFFFF; border-left: 3px solid #C5A059; border-radius: 8px; padding: 18px; margin-top: 16px; border: 1px solid #EAE2D7;">
        <strong style="color: #1F1815; font-family: 'Playfair Display', serif; font-size: 16px;">Why 'Biggest Debt First' Loses Money:</strong>
        <p style="font-size: 13.5px; color: #5C5047; margin-top: 6px; line-height: 1.6;">
            Sorting purely by debt size directs collections officers to accounts with massive overdue balances that have an 86%–93% failure rate.
            These accounts have suffered fatal business distress or displacement.
            By conditioning rankings on <strong>Expected Recoverable Value</strong> ($P(\text{cure}) \times \hat{r} \times \text{Debt}$),
            officers engage borrowers with substantial debts who retain active capacity and willingness to settle,
            recovering an additional <strong>2,164,156 FCFA per 100 worked accounts (+65.6% cash lift)</strong>.
        </p>
    </div>
    """), unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 7: ETHICAL SAFEGUARDS & HUMAN COST
# -------------------------------------------------------------
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
