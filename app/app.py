"""Streamlit Production Web App: Loan Collections Prioritiser (Bamenda MFI).

Built for 3 Collections Officers (John, Beatrice, Emmanuel) in Bamenda, Cameroon.
Features:
- Live ranked weekly list of 400 arrears accounts.
- Filter by Collections Officer, Contact Method, and Vulnerability Flag.
- Executive KPI bar showing total arrears, expected recovery, net value, and lift vs incumbent.
- Actionable reasons for each recommendation.
- Ethical safeguard module protecting vulnerable borrowers from aggressive collection.
- Mobile-optimized layout for collections officers in the field.
"""
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Collections Prioritiser | Bamenda MFI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "weekly_400_accounts.csv"
METRICS_PATH = Path(__file__).resolve().parents[1] / "reports" / "metrics_summary.json"


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        st.error(f"Data file not found at {DATA_PATH}. Please run `python run_pipeline.py` first.")
        return pd.DataFrame()
    df = pd.read_csv(DATA_PATH)
    return df


df_raw = load_data()

# Custom CSS for executive styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .badge-call {
        background-color: #e6f4ea;
        color: #137333;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-sms {
        background-color: #e8f0fe;
        color: #1a73e8;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-visit {
        background-color: #fce8e6;
        color: #c5221f;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-vulnerable {
        background-color: #fef7e0;
        color: #b06000;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📋 Loan Collections Prioritiser")
st.caption("AI-Powered Recovery Decision Support System | Microfinance Institution — Bamenda, Cameroon")

if df_raw.empty:
    st.stop()

# Sidebar: Filters & Controls
with st.sidebar:
    st.header("⚙️ Workload & Filters")
    
    officers = ["All Officers"] + sorted(df_raw["assigned_officer"].unique().tolist())
    selected_officer = st.selectbox("Assigned Officer", officers)
    
    channels = ["All Channels"] + sorted(df_raw["recommended_channel"].unique().tolist())
    selected_channel = st.selectbox("Contact Channel", channels)
    
    vulnerability_filter = st.radio(
        "Ethical Safeguard Filter",
        ["All Accounts", "Standard Accounts Only", "Protected / Vulnerable Only"]
    )
    
    min_prob = st.slider("Min Recovery Probability", 0.0, 1.0, 0.0, 0.05)
    
    st.markdown("---")
    st.markdown("### 🏛️ Bamenda Operations")
    st.markdown("""
    - **Active Officers:** 3 full-time
    - **Weekly Capacity:** ~100-130 contacts/officer
    - **SMS Cost:** 50 FCFA
    - **Call Cost:** 500 FCFA
    - **Field Visit Cost:** 5,000 FCFA
    """)
    st.markdown("---")
    st.caption("Skye8 Company Ltd | Final Project SKY8-DS-FP-005")

# Filter data
filtered_df = df_raw.copy()

if selected_officer != "All Officers":
    filtered_df = filtered_df[filtered_df["assigned_officer"] == selected_officer]

if selected_channel != "All Channels":
    filtered_df = filtered_df[filtered_df["recommended_channel"] == selected_channel]

if vulnerability_filter == "Standard Accounts Only":
    filtered_df = filtered_df[~filtered_df["is_vulnerable"]]
elif vulnerability_filter == "Protected / Vulnerable Only":
    filtered_df = filtered_df[filtered_df["is_vulnerable"]]

filtered_df = filtered_df[filtered_df["recovery_probability"] >= min_prob]

# Executive Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

total_overdue = filtered_df["overdue_amount"].sum()
expected_rec = filtered_df["expected_gross_recovery_fcfa"].sum()
total_cost = filtered_df["channel_cost_fcfa"].sum()
net_rec = expected_rec - total_cost
avg_prob = filtered_df["recovery_probability"].mean() if len(filtered_df) > 0 else 0

with col1:
    st.metric("Arrears Portfolio", f"{total_overdue:,.0f} FCFA", f"{len(filtered_df)} Accounts")
with col2:
    st.metric("Expected Recovery", f"{expected_rec:,.0f} FCFA", f"{expected_rec/max(1.0, total_overdue):.1%} of debt")
with col3:
    st.metric("Outreach Action Cost", f"{total_cost:,.0f} FCFA", f"Net: {net_rec:,.0f} FCFA")
with col4:
    st.metric("Precision @ 100", "87.0%", "+80.0% vs Incumbent")
with col5:
    st.metric("Value Added (Lift)", "+2,112,657 FCFA", "+64.0% vs Debt-First")

st.markdown("---")

# Main View: Tabs
tab_ranked, tab_insights, tab_ethics = st.tabs(["📋 Prioritised Call Book", "📊 Financial & ML Metrics", "🛡️ Ethical Safeguards & Human Cost"])

with tab_ranked:
    st.subheader(f"Ranked Worklist ({len(filtered_df)} Accounts Selected)")
    st.write("Ranked by **Expected Recoverable Value** ($P(\\text{recovery}) \\times \\text{Debt}$). Highest recoverable yields first.")
    
    display_cols = [
        "rank", "SK_ID_CURR", "assigned_officer", "overdue_amount",
        "recovery_probability", "recommended_channel", "channel_cost_fcfa",
        "is_vulnerable", "action_reason"
    ]
    
    format_dict = {
        "overdue_amount": "{:,.0f} FCFA",
        "recovery_probability": "{:.1%}",
        "channel_cost_fcfa": "{:,.0f} FCFA"
    }
    
    st.dataframe(
        filtered_df[display_cols].style.format(format_dict),
        use_container_width=True,
        height=450
    )
    
    # Borrower Detail Inspector
    st.subheader("🔍 Account Deep Dive")
    selected_account = st.selectbox(
        "Select Account ID for Details",
        filtered_df["SK_ID_CURR"].tolist() if not filtered_df.empty else []
    )
    
    if selected_account:
        acc = filtered_df[filtered_df["SK_ID_CURR"] == selected_account].iloc[0]
        
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        with detail_col1:
            st.markdown(f"**Borrower ID:** `{acc['SK_ID_CURR']}`")
            st.markdown(f"**Loan Ref (Previous):** `{acc['SK_ID_PREV']}`")
            st.markdown(f"**Assigned Officer:** {acc['assigned_officer']}")
            st.markdown(f"**Overdue Debt:** `{acc['overdue_amount']:,.0f} FCFA`")
            
        with detail_col2:
            st.markdown(f"**Recovery Probability:** `{acc['recovery_probability']:.1%}`")
            st.markdown(f"**Prior Late Payment Ratio:** `{acc['prior_late_ratio']:.1%}`")
            st.markdown(f"**Prior Late Installments:** `{int(acc['prior_late_count'])}`")
            st.markdown(f"**Prior Severe Delinquencies (15+ days):** `{int(acc['prior_severe_late_count'])}`")
            
        with detail_col3:
            st.markdown(f"**Recommended Channel:** `{acc['recommended_channel']}` ({acc['channel_cost_fcfa']:,.0f} FCFA)")
            st.markdown(f"**Expected Net Yield:** `{acc['expected_net_recovery_fcfa']:,.0f} FCFA`")
            st.markdown(f"**Vulnerability Flag:** `{'YES (Protected)' if acc['is_vulnerable'] else 'NO (Standard)'}`")
            st.info(f"💡 **Action Rationale:** {acc['action_reason']}")

with tab_insights:
    st.subheader("📈 Performance Benchmark: ML Prioritiser vs Incumbent Heuristic")
    
    col_bench1, col_bench2 = st.columns(2)
    with col_bench1:
        st.markdown("#### Precision Comparison (Accounts Cured / Contacted)")
        st.write("Officers work top-50 to top-100 accounts per week.")
        
        perf_data = pd.DataFrame({
            "Policy": ["ML Prioritiser (Expected Value)", "Incumbent (Biggest Debt First)", "Random Baseline (Unassisted)"],
            "Precision @ 50": [0.90, 0.14, 0.18],
            "Precision @ 100": [0.87, 0.07, 0.17]
        })
        st.table(perf_data.style.format({"Precision @ 50": "{:.1%}", "Precision @ 100": "{:.1%}"}))
        
    with col_bench2:
        st.markdown("#### Total Money Recovered Comparison (Francs CFA)")
        st.write("Actual cash collected under each ranking order.")
        
        money_data = pd.DataFrame({
            "Policy": ["ML Prioritiser (Expected Value)", "Incumbent (Biggest Debt First)", "Net Financial Lift"],
            "Top 50 Accounts": ["4,529,712 FCFA", "3,301,388 FCFA", "+1,228,324 FCFA (+37.2%)"],
            "Top 100 Accounts": ["5,414,045 FCFA", "3,301,388 FCFA", "+2,112,657 FCFA (+64.0%)"]
        })
        st.table(money_data)

    st.markdown("""
    > **Key Insight:** Biggest-debt-first targets borrowers who owe huge sums but have a 90%+ default likelihood (insolvent/ghost accounts).
    > The ML Prioritiser targets borrowers who owe substantial sums **and** have strong underlying recovery capacity, unlocking **+2.11M FCFA extra recovery per 100 accounts**.
    """)

with tab_ethics:
    st.subheader("🛡️ Ethical Safeguards & The Human Cost of Collections")
    st.markdown("""
    ### Why Collections Requires Humanitarian Guardrails
    Microfinance borrowers in Bamenda are smallholders, traders, teachers, and artisans often facing external economic shocks:
    - **Health shocks & bereavement**
    - **Crop failure or market disruptions**
    - **Regional security instability in the North West Region**
    
    A tool that merely maximizes debt pressure pushes collections officers toward predatory harassment, which destroys institutional trust and client livelihoods.

    ### Built-in Safety Features in This Product:
    1. **Vulnerability Detection:**
       - Borrowers age 60+ are flagged for **Senior Hardship Review**.
       - Borrowers with documented employment disruption are flagged for **Income Stabilization Inquiry**.
       - Severe distress accounts are diverted to **Restructuring & Grace Period**, not Field Enforcement.
    2. **Field Visit Cost/Benefit Threshold:**
       - Field visits are strictly prohibited on accounts under 25,000 FCFA or vulnerable clients.
    3. **Tone & Script Guidance:**
       - The system generates cooperative negotiation scripts ("How can we restructure your payment plan?") rather than aggressive demand notices.
    """)

st.caption("Developed by Nahbila Faith | Skye8 Company Ltd Data Science Final Project (SKY8-DS-FP-005) | Bamenda, Cameroon")
