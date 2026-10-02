"""Skye8 Collections Prioritiser — Haute-Elegance Editorial Edition.

A high-luxury, editorial UI/UX designed for Microfinance Institutions in Bamenda, Cameroon.
Features:
- Super elegant luxury sidebar with officer load distribution, channels, and system telemetry.
- Editorial typography (Playfair Display & Plus Jakarta Sans).
- Warm espresso, champagne gold, and ivory silk palette.
- Bespoke KPI metric cards and micro-interactions.
- Dossier-style account deep-dive inspector with human-dignity safeguarding.
- Mobile-responsive, high-craft aesthetics.
"""
from pathlib import Path
import textwrap
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration - Super elegant sidebar open by default
st.set_page_config(
    page_title="Skye8 Prioritiser | Haute Edition",
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

# Inject High-Luxury Editorial CSS including Super Elegant Dark Sidebar
st.markdown(textwrap.dedent("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Global Resets & Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        color: #231C18;
        background-color: #FAF8F5;
    }
    
    .stApp {
        background-color: #FAF8F5;
    }

    /* ========================================================
       SUPER ELEGANT SIDEBAR (NOIR ESPRESSO & CHAMPAGNE GOLD)
       ======================================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16110F 0%, #1D1613 60%, #241B17 100%) !important;
        border-right: 1px solid rgba(197, 160, 89, 0.22) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #E8DDD4 !important;
    }

    section[data-testid="stSidebar"] label {
        font-size: 10.5px !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        color: #C5A059 !important;
    }

    /* Style selectboxes and inputs inside sidebar */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(197, 160, 89, 0.3) !important;
        border-radius: 8px !important;
        color: #FAF8F5 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FAF8F5 !important;
    }

    .sidebar-brand-block {
        padding: 8px 4px 20px 4px;
        border-bottom: 1px solid rgba(197, 160, 89, 0.22);
        margin-bottom: 24px;
    }

    .sidebar-crest {
        font-size: 28px;
        line-height: 1;
        margin-bottom: 8px;
    }

    .sidebar-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 0.06em;
        color: #FAF8F5;
        margin: 0;
    }

    .sidebar-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 9.5px;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #C5A059;
        margin-top: 5px;
        font-weight: 500;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(197, 160, 89, 0.2);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 22px;
    }

    .sidebar-card-title {
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #C5A059;
        font-weight: 600;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .sidebar-stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        padding: 6px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .sidebar-stat-row:last-child {
        border-bottom: none;
    }

    .sidebar-stat-name {
        color: #D6C8BE;
        font-weight: 400;
    }

    .sidebar-stat-val {
        color: #FAF8F5;
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
        padding: 5px 10px;
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
        background: linear-gradient(135deg, #1C1512 0%, #2A201B 60%, #382B24 100%);
        border-radius: 16px;
        padding: 44px 44px 38px 44px;
        margin-bottom: 30px;
        color: #FAF8F5;
        position: relative;
        box-shadow: 0 20px 40px rgba(28, 21, 18, 0.12);
        border: 1px solid rgba(197, 160, 89, 0.25);
    }
    
    .hero-eyebrow {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #C5A059;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .hero-eyebrow::before {
        content: "";
        width: 18px;
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
        color: #FAF8F5;
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
        line-height: 1.6;
        color: #D3C7BF;
        max-width: 640px;
        font-weight: 300;
    }

    /* Executive KPI Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 32px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #EAE3DA;
        border-radius: 12px;
        padding: 22px 20px;
        box-shadow: 0 4px 16px rgba(44, 34, 28, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(44, 34, 28, 0.06);
        border-color: #C5A059;
    }

    .metric-label {
        font-size: 10.5px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #8C7E75;
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
        font-size: 11.5px;
        font-weight: 500;
        color: #9E7438;
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
        border: 1px solid #EAE3DA;
        border-radius: 14px;
        padding: 28px;
        margin-top: 16px;
        box-shadow: 0 8px 30px rgba(44, 34, 28, 0.04);
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
        border-bottom: 1px solid #F0EAE2;
        padding-bottom: 16px;
        margin-bottom: 20px;
    }

    .dossier-id {
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        color: #1F1815;
    }

    .dossier-meta {
        font-size: 12px;
        color: #8C7E75;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Refined Streamlit Native Overrides */
    div[data-baseweb="tab-list"] {
        border-bottom: 1px solid #E6DED5 !important;
        gap: 24px !important;
    }

    button[data-baseweb="tab"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 17px !important;
        color: #7D7268 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 12px 4px !important;
    }

    button[aria-selected="true"] {
        color: #1F1815 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #C5A059 !important;
    }

    .dataframe {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 13px !important;
    }
</style>
"""), unsafe_allow_html=True)

if df_raw.empty:
    st.error("Weekly portfolio data not found. Please run `python run_pipeline.py` first.")
    st.stop()

# =============================================================
# SUPER ELEGANT SIDEBAR (EXECUTIVE CONTROLS & TELEMETRY)
# =============================================================
with st.sidebar:
    st.markdown(textwrap.dedent("""
    <div class="sidebar-brand-block">
        <div class="sidebar-crest">⚜️</div>
        <h2 class="sidebar-title">SKYE8 PRIORITISER</h2>
        <div class="sidebar-subtitle">Haute Collections Intelligence &bull; Bamenda</div>
        <div class="sidebar-status-pill">
            <span class="pulse-dot"></span>
            Model Active &bull; Zero Leakage
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

    st.markdown("---")
    
    # Live Officer Capacity Card
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
            <span class="sidebar-stat-name">SMS Prompt</span>
            <span class="sidebar-stat-val">50 FCFA</span>
        </div>
        <div class="sidebar-stat-row">
            <span class="sidebar-stat-name">Phone Call</span>
            <span class="sidebar-stat-val">500 FCFA</span>
        </div>
        <div class="sidebar-stat-row">
            <span class="sidebar-stat-name">Field Visit</span>
            <span class="sidebar-stat-val">5,000 FCFA</span>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
    <div style="font-size: 10px; color: #8C7E75; text-align: center; letter-spacing: 0.1em; text-transform: uppercase;">
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
# EXECUTIVE KPI METRICS (BESPOKE HTML GRID)
# -------------------------------------------------------------
total_overdue = df_filtered["overdue_amount"].sum()
expected_rec = df_filtered["expected_gross_recovery_fcfa"].sum()
total_cost = df_filtered["channel_cost_fcfa"].sum()
net_rec = expected_rec - total_cost

st.markdown(textwrap.dedent(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Active Arrears Book</div>
        <div class="metric-value">{total_overdue:,.0f} <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#8C7E75;">FCFA</span></div>
        <div class="metric-badge">{len(df_filtered)} Active Accounts</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Expected Recovery</div>
        <div class="metric-value">{expected_rec:,.0f} <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#8C7E75;">FCFA</span></div>
        <div class="metric-badge">{expected_rec/max(1.0, total_overdue):.1%} of Delinquent Balance</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Action Cost & Net</div>
        <div class="metric-value">{net_rec:,.0f} <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#8C7E75;">FCFA</span></div>
        <div class="metric-badge">Outreach Cost: {total_cost:,.0f} FCFA</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Precision @ 100 Accounts</div>
        <div class="metric-value">87.0%</div>
        <div class="metric-badge">12.4x vs Incumbent Heuristic (7.0%)</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Net Financial Lift</div>
        <div class="metric-value">+2,112,657 <span style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#8C7E75;">FCFA</span></div>
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

# TAB 1: BESPOKE DOSSIER INSPECTOR
with tab_dossier:
    st.markdown("### Client Dossier & Actionable Guidance")
    st.caption("Select a borrower account to inspect their historical payment trajectory, recovery probability, and field contact script.")
    
    selected_account = st.selectbox(
        "Select Account Number",
        df_filtered["SK_ID_CURR"].tolist() if not df_filtered.empty else []
    )
    
    if selected_account:
        acc = df_filtered[df_filtered["SK_ID_CURR"] == selected_account].iloc[0]
        
        channel_tag_class = "tag-sms" if acc["recommended_channel"] == "SMS" else ("tag-call" if acc["recommended_channel"] == "CALL" else "tag-visit")
        vulnerable_tag = f'<span class="tag-vulnerable">Protected &bull; Senior / Hardship</span>' if acc["is_vulnerable"] else '<span class="tag-sms">Standard Operational Flow</span>'
        
        # Render clean, dedented HTML to prevent markdown from turning it into a pre/code block
        dossier_html = textwrap.dedent(f"""
        <div class="dossier-card">
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
                    <div style="font-size: 11px; color: #8C7E75;">15 Days Past Due</div>
                </div>
                <div>
                    <div class="metric-label">Recovery Probability</div>
                    <div style="font-size: 20px; font-weight: 600; color: #C5A059;">{acc['recovery_probability']:.1%}</div>
                    <div style="font-size: 11px; color: #8C7E75;">Calibrated ML Estimate</div>
                </div>
                <div>
                    <div class="metric-label">Assigned Officer</div>
                    <div style="font-size: 18px; font-weight: 600; color: #1F1815;">{acc['assigned_officer']}</div>
                    <div style="font-size: 11px; color: #8C7E75;">Mezam / Bamenda Unit</div>
                </div>
                <div>
                    <div class="metric-label">Net Yield Expectation</div>
                    <div style="font-size: 20px; font-weight: 600; color: #2E5A36;">{acc['expected_net_recovery_fcfa']:,.0f} FCFA</div>
                    <div style="font-size: 11px; color: #8C7E75;">Net of Action Cost ({acc['channel_cost_fcfa']:,.0f} FCFA)</div>
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
                    <div style="background-color: #FAF8F5; border: 1px solid #EAE3DA; border-radius: 8px; padding: 14px; margin-top: 6px;">
                        <div style="font-size: 13px; font-weight: 600; color: #1F1815; margin-bottom: 4px;">Strategic Reasoning:</div>
                        <div style="font-size: 12.5px; color: #5C5047; line-height: 1.5; margin-bottom: 10px;">{acc['action_reason']}</div>
                        <div style="font-size: 13px; font-weight: 600; color: #1F1815; margin-bottom: 4px;">Recommended Dialogue Tone:</div>
                        <div style="font-size: 12.5px; color: #5C5047; font-style: italic;">
                            "{'Acknowledge customer loyalty, verify hardship context, and offer flexible 14-day instalment restructuring.' if acc['is_vulnerable'] else 'Polite notification of 15-day arrears mark; confirm commitment to settle within 30-day grace cycle.'}"
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """)
        st.markdown(dossier_html, unsafe_allow_html=True)

# TAB 2: PRIORITISED TABLE VIEW
with tab_table:
    st.markdown("### Weekly Prioritised Call Book (400 Accounts)")
    st.caption("Ordered by Expected Recoverable Cash Flow (P(recovery) × Debt). Prioritizing high-probability, high-yield accounts first.")
    
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
    <div style="background-color: #FFFFFF; border-left: 3px solid #C5A059; border-radius: 8px; padding: 18px; margin-top: 16px; border: 1px solid #EAE3DA;">
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
        <div style="background: #FFFFFF; border: 1px solid #EAE3DA; border-radius: 12px; padding: 20px;">
            <div style="font-size: 32px; font-family: 'Playfair Display', serif; color: #8D5B18; font-weight: 600;">74 Borrowers</div>
            <div style="font-size: 12px; color: #8C7E75; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">Protected by Ethical Filters (18.5%)</div>
            <div style="font-size: 12.5px; color: #5C5047; line-height: 1.6;">
                These accounts have been diverted from aggressive visits to friendly restructuring dialogues.
                Overdue balances are preserved without inflicting humanitarian harm on distressed families.
            </div>
        </div>
        """), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(textwrap.dedent("""
<div style="display: flex; justify-content: space-between; font-size: 11px; color: #8C7E75; letter-spacing: 0.08em; text-transform: uppercase;">
    <div>Skye8 Company Ltd &bull; Final Project SKY8-DS-FP-005</div>
    <div>Candidate: Nahbila Faith &bull; Bamenda, Cameroon</div>
</div>
"""), unsafe_allow_html=True)
