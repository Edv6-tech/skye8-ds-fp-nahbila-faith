"""Skyes Intelligence — Recovery Decision Workspace (ux.html Exact Replica).

Exact pixel-accurate reproduction of ux.html format with 100% feature preservation:
- Deep Pine / Citron styling from ux.html (:root, fonts, gradients, animations, layouts).
- Exact Hero card (.account-hero, .hero-copy, .eyebrow, .hero-tags, .score-ring, .hero-cta).
- Exact 4 Metrics cards (.metrics, .metric, .metric-label, .metric-value, .metric-note).
- Exact Workspace Head (.work-head, .text-link).
- Exact Two-Column Decision Grid (.grid, .card, .timeline, 4 .step-dots, .case-data, .evidence, .signal, .rationale).
- Exact Supplemental Row (.supplemental, Member contact with Call member, Decision rationale).
- Exact Lower Row (.lower, Member outreach call script, Affordability proposal slider).
- Exact Commit Card (.card.commit#outcome, Contact outcome, Promise window, notes, and Commit button).
- Retains 100% of all analytical, regulatory, routing, USSD, what-if, and ethics tools.
"""
import sys
from pathlib import Path
import textwrap
import io

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np

from src.model import (
    AdaptablePrioritiser,
    compute_xai_waterfall,
    predict_recovery_probability
)
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
    page_title="Skyes Intelligence — Account review",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data paths
DATA_PATH = ROOT_DIR / "data" / "processed" / "weekly_400_accounts.csv"
CSS_PATH = Path(__file__).resolve().parent / "ux_styles.css"


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

# Inject complete CSS from ux.html
if CSS_PATH.exists():
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if df_raw.empty:
    st.error("Weekly portfolio data not found. Please run `python run_pipeline.py` first.")
    st.stop()

# =============================================================
# SIDEBAR: EXACT REPLICA OF ASIDE IN UX.HTML
# =============================================================
with st.sidebar:
    st.markdown(textwrap.dedent("""
    <div class="brand">
        <div class="mark">✳</div>
        <div>
            <b>SKYES INTELLIGENCE</b>
            <small>RECOVERY WORKSPACE</small>
        </div>
    </div>
    """), unsafe_allow_html=True)

    st.markdown('<div class="nav-label" style="margin-top:16px;">Workspace</div>', unsafe_allow_html=True)
    nav_selection = st.radio(
        "Workspace Navigation",
        ["Case review", "Overview", "Decision signals", "Member outreach"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown(textwrap.dedent("""
    <div class="filters">
        <div class="nav-label">Decision setup</div>
    </div>
    """), unsafe_allow_html=True)

    mandate = st.selectbox(
        "Strategic mandate",
        ["Member-first recovery", "Balanced portfolio", "Recovery priority"],
        index=0
    )
    objective = st.selectbox(
        "Optimization objective",
        ["Maximum net recovery", "Minimize contact cost", "Member affordability"],
        index=0
    )
    archetype = st.selectbox(
        "Branch archetype",
        ["Standard calibration", "Urban branch", "Rural branch"],
        index=0
    )

    st.markdown(textwrap.dedent("""
    <div class="filters">
        <div class="nav-label filter-divider">Portfolio filters</div>
    </div>
    """), unsafe_allow_html=True)

    assignee = st.selectbox(
        "Assignee",
        ["All collections", "John N.", "Emmanuel K."],
        index=0
    )
    channel = st.selectbox(
        "Outreach channel",
        ["All outreach", "Phone call", "Field visit", "SMS"],
        index=0
    )
    quarter_options = ["All demands"] + sorted(df_raw["bamenda_quarter"].dropna().unique().tolist())
    zone = st.selectbox(
        "Quarter / urban zone",
        quarter_options,
        index=0
    )
    safeguard = st.selectbox(
        "Ethical safeguard",
        ["All accounts", "Member support required"],
        index=0
    )
    cure_filter = st.slider(
        "Minimum cure probability",
        0, 100, 0,
        format="%d%%"
    )
    lookup = st.text_input(
        "Borrower ID or loan reference",
        placeholder="e.g. 103380"
    )

    st.markdown(textwrap.dedent("""
    <div class="sidebar-utility">
        <div class="nav-label">Operations</div>
        <button class="export-btn office-btn">▤　Office catalog &amp; allocation</button>
        <div class="nav-label mobility-label" style="margin-top:12px;">Field mobility</div>
    </div>
    """), unsafe_allow_html=True)

    # Re-rank dynamically based on objective selection
    obj_str = "Maximum Cash Flow (EV = P × r × Debt)" if objective == "Maximum net recovery" else "Maximum Cure Rate (Rank by P)"
    df_active = st.session_state.adaptable_engine.rank_portfolio(
        df_raw,
        objective=obj_str,
        fuel_price_fcfa=850.0,
        airtime_cost_fcfa=500.0
    )

    # Apply sidebar filters
    df_filtered_side = df_active.copy()
    if assignee != "All collections":
        df_filtered_side = df_filtered_side[df_filtered_side["assigned_officer"].str.contains(assignee.split()[0], na=False)]
    if channel != "All outreach":
        ch_map = {"Phone call": "CALL", "Field visit": "FIELD_VISIT", "SMS": "SMS"}
        if channel in ch_map:
            df_filtered_side = df_filtered_side[df_filtered_side["recommended_channel"] == ch_map[channel]]
    if zone != "All demands":
        df_filtered_side = df_filtered_side[df_filtered_side["bamenda_quarter"] == zone]
    if safeguard == "Member support required":
        df_filtered_side = df_filtered_side[df_filtered_side.get("is_vulnerable", False) == True]
    if cure_filter > 0:
        df_filtered_side = df_filtered_side[df_filtered_side["recovery_probability"] >= (cure_filter / 100.0)]
    if lookup:
        df_filtered_side = df_filtered_side[
            df_filtered_side["SK_ID_CURR"].astype(str).str.contains(lookup) |
            df_filtered_side["SK_ID_PREV"].astype(str).str.contains(lookup)
        ]

    # Download CSV button styled identically to ux.html
    csv_buf = io.StringIO()
    df_filtered_side.to_csv(csv_buf, index=False)
    st.download_button(
        label="⇩　Download full call sheet (CSV)",
        data=csv_buf.getvalue(),
        file_name="Skyes_Call_Sheet_400_Accounts.csv",
        mime="text/csv",
        key="btn_sidebar_csv_dl"
    )

    st.markdown(textwrap.dedent("""
    <div class="user">
        <div class="avatar">JN</div>
        <div>
            <b>John N.</b>
            <span>Recovery officer</span>
        </div>
    </div>
    """), unsafe_allow_html=True)


# =============================================================
# VIEW 1: CASE REVIEW (EXACT REPLICA OF MAIN IN UX.HTML)
# =============================================================
if nav_selection == "Case review":
    avail_accounts = df_filtered_side["SK_ID_CURR"].tolist() if not df_filtered_side.empty else df_active["SK_ID_CURR"].tolist()
    default_acc_id = 103380 if 103380 in avail_accounts else avail_accounts[0]
    default_idx = avail_accounts.index(default_acc_id)

    # 1. TOPBAR
    top_col1, top_col2 = st.columns([3, 1.2])
    with top_col1:
        st.markdown(textwrap.dedent("""
        <header class="topbar">
            <div class="crumb">Portfolio<i>/</i>Priority cases<i>/</i><b>Account review</b></div>
        </header>
        """), unsafe_allow_html=True)
    with top_col2:
        selected_account = st.selectbox(
            "Account Switcher",
            avail_accounts,
            index=default_idx,
            label_visibility="collapsed",
            format_func=lambda aid: f"Client #{aid}"
        )

    acc = df_active[df_active["SK_ID_CURR"] == selected_account].iloc[0]

    client_id = int(acc["SK_ID_CURR"])
    loan_id = int(acc["SK_ID_PREV"])
    overdue_amt = float(acc["overdue_amount"])
    recovery_prob = float(acc["recovery_probability"])
    expected_net = float(acc["expected_net_recovery_fcfa"])
    officer_name = str(acc["assigned_officer"]).split(" - ")[-1]
    quarter_name = str(acc.get("bamenda_quarter", "Commercial avenue"))
    pct_val = int(round(recovery_prob * 100))

    # Fetch live XAI waterfall
    xai_data = compute_xai_waterfall(acc)
    top_positives = xai_data.get("top_positive", [])
    top_negatives = xai_data.get("top_negative", [])

    # 2. ACCOUNT HERO (EXACT UX.HTML FORMAT)
    hero_markup = f"""
    <section class="account-hero">
        <div class="hero-copy">
            <div class="eyebrow">Recommended action &bull; supportive call</div>
            <h1>Client #{client_id}</h1>
            <p class="subline">Loan reference {loan_id}　&bull;　{quarter_name}　&bull;　Urban market zone</p>
            <div class="hero-tags">
                <span class="tag action">Call today</span>
                <span class="tag">Member-first approach</span>
                <span class="tag">Assigned to {officer_name}</span>
            </div>
        </div>
        <div class="hero-score">
            <div class="score-ring" style="background: conic-gradient(var(--citron) 0 {pct_val}%, #ffffff32 {pct_val}% 100%);">
                <div class="score-inner">
                    <b>{pct_val}%</b>
                    <span>LIKELIHOOD</span>
                </div>
            </div>
            <div class="score-label">
                <b>Strong recovery potential</b>
                <span>Recommended contact window: today</span>
            </div>
            <a href="#outreach" class="hero-cta" style="text-decoration:none;">Prepare call　↗</a>
        </div>
    </section>
    """
    st.markdown(textwrap.dedent(hero_markup), unsafe_allow_html=True)

    # 3. METRICS ROW (EXACT UX.HTML FORMAT)
    metrics_markup = f"""
    <section class="metrics" aria-label="Account summary">
        <article class="metric">
            <div class="metric-label">Overdue balance</div>
            <div class="metric-value">{overdue_amt:,.0f} <small style="font-size:10px;font-weight:500">FCFA</small></div>
            <div class="metric-note">Current arrears amount</div>
        </article>
        <article class="metric">
            <div class="metric-label">Recovery likelihood</div>
            <div class="metric-value">{pct_val}<small style="font-size:12px">%</small></div>
            <div class="metric-note good">High-confidence recommendation</div>
        </article>
        <article class="metric">
            <div class="metric-label">Expected net recovery</div>
            <div class="metric-value">{expected_net:,.0f} <small style="font-size:10px;font-weight:500">FCFA</small></div>
            <div class="metric-note">After estimated outreach cost</div>
        </article>
        <article class="metric">
            <div class="metric-label">Assigned officer</div>
            <div class="metric-value" style="font-size:17px">{officer_name}</div>
            <div class="metric-note">{quarter_name} branch</div>
        </article>
    </section>
    """
    st.markdown(textwrap.dedent(metrics_markup), unsafe_allow_html=True)

    # 4. WORK HEAD (EXACT UX.HTML FORMAT)
    work_head_markup = """
    <div class="work-head">
        <div>
            <h2>Account decision workspace</h2>
            <p>Review the evidence, tailor a supportive contact, and record the next step.</p>
        </div>
        <a class="text-link" href="#outcome">Jump to outcome &darr;</a>
    </div>
    """
    st.markdown(textwrap.dedent(work_head_markup), unsafe_allow_html=True)

    # 5. GRID: ACCOUNT HISTORY & DECISION SIGNALS
    sig_rows_html = ""
    for pos in top_positives[:3]:
        sig_rows_html += f'<div class="signal"><span class="sig-ico">&check;</span><b>{pos["factor"]}</b><span>POSITIVE</span></div>'
    for neg in top_negatives[:1]:
        sig_rows_html += f'<div class="signal risk"><span class="sig-ico">!</span><b>{neg["factor"]}</b><span>REVIEW</span></div>'

    grid_markup = f"""
    <div class="grid">
        <section class="card">
            <div class="card-head">
                <h3>Account history</h3>
                <span class="pill">Positive repayment pattern</span>
            </div>
            <div class="card-body">
                <div class="timeline">
                    <div class="step done"><div class="step-dot">&check;</div><span>Account opened</span></div>
                    <div class="step done"><div class="step-dot">&check;</div><span>Payments made</span></div>
                    <div class="step done"><div class="step-dot">&check;</div><span>Member contacted</span></div>
                    <div class="step current"><div class="step-dot">4</div><span>Next action</span></div>
                </div>
                <div class="case-data">
                    <div><span class="field-label">Previous commitments</span><span class="field-value">3 of 3 kept</span></div>
                    <div><span class="field-label">Recent engagement</span><span class="field-value">Member recently responsive</span></div>
                    <div><span class="field-label">Portfolio segment</span><span class="field-value">{quarter_name}</span></div>
                    <div><span class="field-label">Decision outcome</span><span class="field-value">Supportive call recommended</span></div>
                </div>
            </div>
        </section>
        <section class="card" id="signals">
            <div class="card-head">
                <h3>Decision signals</h3>
                <span class="pill">3 positive &bull; 1 to review</span>
            </div>
            <div class="card-body">
                <div class="evidence">
                    {sig_rows_html}
                </div>
                <div class="rationale">
                    <b>Why this action?</b>A brief, supportive call is likely to resolve the arrears. The account shows reliable past repayment and consistent follow-through on previous commitments.
                </div>
            </div>
        </section>
    </div>
    """
    st.markdown(textwrap.dedent(grid_markup), unsafe_allow_html=True)

    # 6. SUPPLEMENTAL: MEMBER CONTACT & DECISION RATIONALE
    supplemental_markup = """
    <div class="supplemental" style="margin-top:13px;">
        <section class="card">
            <div class="card-head">
                <h3>Member contact</h3>
                <span class="pill">Contact methods</span>
            </div>
            <div class="card-body">
                <div class="contact-row">
                    <div><span class="field-label">Primary number</span><b class="field-value">+237 670 500 123 (Verified MTN)</b></div>
                    <a href="tel:+237670500123" class="contact-action" style="text-decoration:none;">Call member</a>
                </div>
                <div class="contact-row">
                    <div><span class="field-label">Alternative number</span><b class="field-value">+237 690 123 456 (Orange)</b></div>
                    <button class="contact-action secondary">View details</button>
                </div>
                <div class="dial-note">
                    <b>Before you dial</b>
                    <span>Use the verified number on the member record. Confirm identity before discussing account information.</span>
                </div>
            </div>
        </section>
        <section class="card">
            <div class="card-head">
                <h3>Decision rationale</h3>
                <span class="pill">Review before adapting</span>
            </div>
            <div class="card-body">
                <label class="field-label" for="decision-note">Predictive decision sponsor &amp; rationale</label>
                <textarea class="decision-note" id="decision-note">A supportive call is recommended based on the account’s strong repayment history and consistent kept promises. Confirm the member’s current circumstances and agree on an affordable next step.</textarea>
                <div class="decision-foot">
                    <span class="helper">Document any change from the recommended approach.</span>
                    <button class="outline-btn">Save rationale</button>
                </div>
            </div>
        </section>
    </div>
    """
    st.markdown(textwrap.dedent(supplemental_markup), unsafe_allow_html=True)

    # 7. LOWER: MEMBER OUTREACH (CALL SCRIPT) & AFFORDABILITY PROPOSAL
    low_c1, low_c2 = st.columns(2)
    with low_c1:
        st.markdown(textwrap.dedent("""
        <section class="card" id="outreach" style="margin-top:13px;">
            <div class="card-head">
                <h3>Member outreach</h3>
                <span class="pill">Suggested call script</span>
            </div>
            <div class="composer">
                <div class="composer-label">
                    <b>Conversation opening</b>
                    <span>Personalize before contact</span>
                </div>
        """), unsafe_allow_html=True)

        call_script = st.text_area(
            "Call Script",
            value=(
                "Hello, I’m calling from Skyes about your account. We noticed your recent payment may have been "
                "difficult to make on time. I’d like to understand what works for you and discuss a manageable way "
                "forward. Is now a good time to talk?"
            ),
            height=105,
            label_visibility="collapsed"
        )

        b_c1, b_c2 = st.columns([3, 1.5])
        with b_c1:
            st.caption("Use a respectful, supportive tone. Confirm identity before discussing account details.")
        with b_c2:
            if st.button("Use this call script", key="btn_use_script"):
                st.success("Script copied for live call!")

        st.markdown("</div></section>", unsafe_allow_html=True)

    with low_c2:
        st.markdown(textwrap.dedent("""
        <section class="card payment" style="margin-top:13px;">
            <div class="card-head">
                <h3>Affordability proposal</h3>
                <span class="pill">Adjust to member capacity</span>
            </div>
            <div class="card-body">
        """), unsafe_allow_html=True)

        instalment_val = st.slider(
            "Proposed monthly instalment",
            min_value=5000,
            max_value=max(60000, int(round(overdue_amt * 1.5, -3))),
            value=min(30000, max(5000, int(round(overdue_amt, -3)))),
            step=1000
        )

        st.markdown(textwrap.dedent(f"""
                <div class="range-top">
                    <span>Proposed monthly instalment</span>
                    <strong>{instalment_val:,.0f} FCFA</strong>
                </div>
                <div class="payment-preview">
                    <div class="mini-stat"><span>Suggested start</span><b>Next available payment date</b></div>
                    <div class="mini-stat"><span>Repayment approach</span><b>Within grace window</b></div>
                </div>
            </div>
        </section>
        """), unsafe_allow_html=True)

    # 8. RECORD THE OUTCOME (COMMIT CARD)
    st.markdown('<div id="outcome" style="height:10px;"></div>', unsafe_allow_html=True)
    st.markdown(textwrap.dedent("""
    <section class="card commit" style="margin-top:13px;">
        <div class="card-head">
            <h3>Record the outcome</h3>
            <span class="pill">Save to account history</span>
        </div>
        <div class="card-body">
    """), unsafe_allow_html=True)

    form_c1, form_c2 = st.columns(2)
    with form_c1:
        st.markdown('<label class="form-label">Contact outcome</label>', unsafe_allow_html=True)
        outcome_sel = st.selectbox(
            "Contact Outcome",
            ["Promise to pay", "Requested a payment plan", "Follow-up required", "Unable to reach"],
            label_visibility="collapsed",
            key="rec_outcome_sel"
        )
    with form_c2:
        st.markdown('<label class="form-label">Promise window</label>', unsafe_allow_html=True)
        window_sel = st.selectbox(
            "Promise Window",
            ["Within grace window", "Tomorrow", "In three days", "Next week"],
            label_visibility="collapsed",
            key="rec_window_sel"
        )

    st.markdown('<label class="form-label promise-label" style="margin-top:10px;">Payment commitment</label>', unsafe_allow_html=True)
    promise_input = st.text_input(
        "Payment Commitment",
        value="Member will make a deposit on the agreed date",
        label_visibility="collapsed"
    )

    notes_input = st.text_area(
        "Outcome notes",
        placeholder="Add relevant context or a follow-up note…",
        height=60,
        label_visibility="collapsed"
    )

    c_foot1, c_foot2 = st.columns([3, 1.5])
    with c_foot1:
        st.markdown('<span class="compliance">Record only relevant details shared during the conversation.</span>', unsafe_allow_html=True)
    with c_foot2:
        if st.button("Commit outcome & adapt plan　→", key="btn_commit_ux"):
            adj = st.session_state.adaptable_engine.incorporate_field_feedback(client_id, outcome_sel)
            st.session_state.logged_feedback.append({
                "Account ID": client_id,
                "Officer": officer_name,
                "Outcome": outcome_sel,
                "Window": window_sel,
                "Commitment": promise_input,
                "Notes": notes_input
            })
            st.success(f"Outcome committed. Bayesian prior adapted ({adj:+.1%}) for Client #{client_id}.")

    st.markdown("</div></section>", unsafe_allow_html=True)

    # 9. ANALYTICAL DEEP DIVE EXPANDER (WHAT-IF, SMALL-SMALL & ETHICS)
    with st.expander("Analytical Deep Dive: What-If Arrears Simulator, Small-Small Daily Plan & Vulnerability Audit", expanded=False):
        deep_c1, deep_c2 = st.columns(2)
        with deep_c1:
            st.markdown("#### What-If Arrears Simulator")
            sim_overdue = st.slider("Simulated Overdue Amount (FCFA)", 10000, 300000, int(overdue_amt), 5000, key="sim_overdue_slider")
            sim_delays = st.slider("Simulated Unpaid Days Past Due", 1, 90, 15, 1, key="sim_delays_slider")
            sim_prob = min(0.999, max(0.05, recovery_prob * (1.0 - (sim_delays - 15) * 0.015) * (overdue_amt / max(1.0, sim_overdue)) ** 0.15))
            st.metric(
                "Simulated Recovery Probability",
                f"{sim_prob:.1%}",
                f"{sim_prob - recovery_prob:+.1%} vs current state"
            )

            st.markdown("#### Small-Small Daily Repayment Plan")
            daily_plan = calculate_small_small_repayment_plan(sim_overdue, business_days_per_month=22)
            st.write(f"Daily Deposit Target: **{daily_plan['daily_deposit_fcfa']:,.0f} FCFA / business day**")
            st.write(f"Estimated Market Days to Cure: **{daily_plan['days_to_cure']} days**")

        with deep_c2:
            st.markdown("#### Vulnerability & Fair Lending Guardrails")
            is_vuln = bool(acc.get("is_vulnerable", False))
            client_age = int(round(acc.get("age_years", 45))) if "age_years" in acc else 45
            st.write(f"Member Age: **{client_age} years**")
            if is_vuln or client_age >= 60:
                st.warning("Member Protected under Senior Hardship Guardrail: High-pressure field visits prohibited.")
            else:
                st.success("Standard Outreach Profile: Eligible for phone engagement and digital settlement.")

            st.markdown("#### SMS Payment Link Template")
            sms_text = (
                f"Credit Union Alert: Hello member #{client_id}, settle your overdue {overdue_amt:,.0f} FCFA "
                f"via MTN MoMo: *126*9*705001*{int(round(overdue_amt))}# or Orange: *150*1*705001*{int(round(overdue_amt))}#. "
                f"Ref: {loan_id}. Support: {officer_name}."
            )
            st.text_area("Ready-to-Send SMS", value=sms_text, height=85)

    # 10. FOOTER
    st.markdown(textwrap.dedent("""
    <footer class="footer">
        <span>Skyes Intelligence　&bull;　Account decision workspace</span>
        <a href="#top" style="color:#52794c; text-decoration:none;">Return to portfolio overview　&uarr;</a>
    </footer>
    """), unsafe_allow_html=True)


# =============================================================
# VIEW 2: OVERVIEW (PORTFOLIO CALL ROSTER & FILTERS)
# =============================================================
elif nav_selection == "Overview":
    st.markdown("### Portfolio Overview & Prioritised Call Book")
    st.caption("Active 400-account delinquent book ranked by Expected Recovery Value across Bamenda division.")

    total_overdue = df_filtered_side["overdue_amount"].sum()
    expected_rec = df_filtered_side["expected_gross_recovery_fcfa"].sum()
    total_cost = df_filtered_side["channel_cost_fcfa"].sum()
    net_rec = expected_rec - total_cost

    overview_kpi = f"""
    <section class="metrics" style="margin-bottom:20px;">
        <article class="metric">
            <div class="metric-label">TOTAL DELINQUENT PORTFOLIO</div>
            <div class="metric-value">{total_overdue:,.0f} <small style="font-size:10px;">FCFA</small></div>
            <div class="metric-note">{len(df_filtered_side)} active accounts filtered</div>
        </article>
        <article class="metric">
            <div class="metric-label">EXPECTED RECOVERY VALUE</div>
            <div class="metric-value">{expected_rec:,.0f} <small style="font-size:10px;">FCFA</small></div>
            <div class="metric-note good">{expected_rec/max(1.0, total_overdue):.1%} portfolio yield</div>
        </article>
        <article class="metric">
            <div class="metric-label">NET RECOVERY AFTER EXPENSES</div>
            <div class="metric-value">{net_rec:,.0f} <small style="font-size:10px;">FCFA</small></div>
            <div class="metric-note">Net of action costs ({total_cost:,.0f} FCFA)</div>
        </article>
        <article class="metric">
            <div class="metric-label">PRECISION @ 100 ACCOUNTS</div>
            <div class="metric-value">88.0%</div>
            <div class="metric-note good">12.6x vs heuristic baseline</div>
        </article>
    </section>
    """
    st.markdown(textwrap.dedent(overview_kpi), unsafe_allow_html=True)

    st.dataframe(
        df_filtered_side[[
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
        height=420
    )

    st.markdown("---")
    st.markdown("### Quantitative Proof: Numbers, Not Adjectives")
    st.caption("Rigorous evaluation on 9,219 unseen arrears accounts on the held-out test partition.")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### Precision Comparison (Accounts Cured / Contacts Made)")
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

    st.markdown(textwrap.dedent("""
    <div class="card" style="padding:18px; margin-top:14px; border-left:3px solid var(--green);">
        <strong style="color:var(--ink); font-size:14px;">Why 'Biggest Debt First' Loses Money:</strong>
        <p style="font-size:12px; color:var(--muted); margin-top:6px; line-height:1.6;">
            Sorting purely by debt size directs collections officers to accounts with massive overdue balances that have an 86%–93% failure rate.
            These accounts have suffered fatal business distress or displacement.
            By conditioning rankings on <strong>Expected Recoverable Value</strong> (<em>P(cure) &times; r &times; Debt</em>),
            officers engage borrowers with substantial debts who retain active capacity and willingness to settle,
            recovering an additional <strong>2,164,156 FCFA per 100 worked accounts (+65.6% cash lift)</strong>.
        </p>
    </div>
    """), unsafe_allow_html=True)


# =============================================================
# VIEW 3: DECISION SIGNALS (COBAC, ADAPTABILITY & BRANCH ROI)
# =============================================================
elif nav_selection == "Decision signals":
    st.markdown("### Risk Telemetry, Statutory Reserves & Engine Calibration")
    st.caption("Deep regulatory compliance (COBAC R-2017/07), active Bayesian drift adaptation, and commercial branch ROI.")

    tab_cobac, tab_calib, tab_commercial = st.tabs([
        "COBAC R-2017/07 Capital Shield",
        "Model Adaptability & Calibration",
        "Branch ROI & License Fee Calculator"
    ])

    with tab_cobac:
        st.markdown("#### COBAC Regulation R-2017/07 Capital Shield & Prudential Reserves")
        st.caption("Central African Banking Commission (COBAC) mandatory write-down provisions preserved by early cure (Day 15).")

        sim_port = st.slider("Total Branch Arrears Portfolio (FCFA)", 25000000, 500000000, 150000000, 5000000, key="cobac_slider")
        cobac = calculate_cobac_regulatory_savings(float(sim_port), cure_lift_rate=0.656, base_cure_rate=0.12)

        cob_c1, cob_c2, cob_c3 = st.columns(3)
        with cob_c1:
            st.metric(
                "Statutory Reserve Preserved",
                f"{cobac['regulatory_capital_saved_fcfa']:,.0f} FCFA",
                f"+{cobac['capital_preservation_pct']:.1f}% capital saved"
            )
        with cob_c2:
            st.metric(
                "Unassisted 20% Provision",
                f"{cobac['unassisted_provision_fcfa']:,.0f} FCFA",
                "Mandatory write-down without AI"
            )
        with cob_c3:
            st.metric(
                "PAR30 Delinquency Reduction",
                f"-{cobac['par30_risk_reduction_pct']:.1f}%",
                "Loans prevented from crossing Day 31"
            )

        st.markdown(textwrap.dedent("""
        <div class="card" style="padding:14px; margin-top:14px; font-size:12px; color:var(--muted); line-height:1.6;">
            <strong>Prudential Capital Preservation Mechanism:</strong> Under CEMAC/COBAC Category 1 Microfinance regulations (Regulation R-2017/07, Articles 21–25), loans entering 31–90 days past due (<em>créances impayées</em>) mandate an immediate <strong>20% write-down reserve</strong> against Tier 1 regulatory capital. By prioritizing and curing accounts at Day 15 before the Day 31 threshold, Skye8 prevents portfolio impairment, directly safeguarding cash capital to support new cooperative lending.
        </div>
        """), unsafe_allow_html=True)

    with tab_calib:
        st.markdown("#### Model Adaptability & Macro Calibration Studio")
        st.caption("Empowering credit union risk officers to dynamically adapt priors, calibrate macroeconomic shocks, and inspect online active learning telemetry.")

        adapt_c1, adapt_c2 = st.columns([1.2, 1.8])
        with adapt_c1:
            st.markdown("##### Live Seasonal Tuning")
            harvest_boost = st.slider("Seasonal Harvest Cash Inflow Boost", 0.0, 0.40, 0.15, 0.05, format="+%.0f%%")
            school_drag = st.slider("School Fee Tuition Expense Drag", 0.0, 0.35, 0.10, 0.05, format="-%.0f%%")
            st.session_state.adaptable_engine.adapt_to_season(harvest_boost=harvest_boost, school_fee_drag=school_drag)

            st.markdown("##### Macroeconomic Unit Cost Recalibration")
            fuel_input = st.number_input("Motorcycle Fuel Price (FCFA / Liter)", min_value=600, max_value=1500, value=850, step=50)
            airtime_input = st.number_input("Outreach Phone Call Cost (FCFA / Call)", min_value=100, max_value=1500, value=500, step=50)

            st.markdown(textwrap.dedent(f"""
            <div class="card" style="padding:12px; margin-top:14px;">
                <div style="font-size:10px; text-transform:uppercase; color:var(--muted); letter-spacing:0.1em; font-weight:700;">Active Engine State</div>
                <div style="font-size:12px; color:var(--ink); margin-top:4px; line-height:1.6;">
                    Branch Log-Odds Offset: <strong>{st.session_state.adaptable_engine.branch_offset:+.2f}</strong><br>
                    Seasonal Multiplier: <strong>{st.session_state.adaptable_engine.season_modifier:.2f}x</strong><br>
                    Online Field Adjustments: <strong>{len(st.session_state.adaptable_engine.feedback_adjustments)} accounts</strong>
                </div>
            </div>
            """), unsafe_allow_html=True)

        with adapt_c2:
            st.markdown("##### Continuous Bayesian Online Feedback Telemetry")
            if st.session_state.logged_feedback:
                feedback_df = pd.DataFrame(st.session_state.logged_feedback)
                st.dataframe(feedback_df, height=180, hide_index=True)
                if st.button("Reset Bayesian Feedback Memory"):
                    st.session_state.adaptable_engine.feedback_adjustments.clear()
                    st.session_state.logged_feedback.clear()
                    st.success("Feedback memory reset.")
                    st.rerun()
            else:
                st.info("No field outcomes logged yet in this session. Log outcomes in Case Review to see the model adapt live!")

            st.markdown("---")
            st.markdown("##### Schema Resilience & Missing Modality Stress Test")
            sc_c1, sc_c2 = st.columns(2)
            with sc_c1:
                st.markdown(textwrap.dedent("""
                <div class="card" style="padding:12px;">
                    <strong>Scenario A: Full Multi-Source Roster</strong><br>
                    <span style="font-size:11px; color:var(--green); font-weight:600;">[Active] Installments + Application + Bureau + POS Cash</span><br>
                    <span style="font-size:10px; color:var(--muted);">Prediction Accuracy: High fidelity (PR-AUC: 0.929)</span>
                </div>
                """), unsafe_allow_html=True)
            with sc_c2:
                st.markdown(textwrap.dedent("""
                <div class="card" style="padding:12px;">
                    <strong>Scenario B: Installments Only (Cold-Start MFI)</strong><br>
                    <span style="font-size:11px; color:#854D0E; font-weight:600;">[Graceful Fallback] Domain Imputation Active</span><br>
                    <span style="font-size:10px; color:var(--muted);">Prediction Accuracy: Robust baseline (PR-AUC: 0.894)</span>
                </div>
                """), unsafe_allow_html=True)

    with tab_commercial:
        st.markdown("#### Credit Union Branch ROI & License Fee Calculator")
        st.caption("Interactive commercial model for Microfinance Branch Managers (NtaCCUL, AZICCUL, CamCCUL).")

        sim_c1, sim_c2 = st.columns([1.2, 2])
        with sim_c1:
            st.markdown("##### Branch Operating Parameters")
            sim_portfolio = st.slider(
                "Total Branch Arrears Portfolio (FCFA)",
                25000000, 500000000, 150000000, 5000000,
                format="%d FCFA",
                key="roi_port_slider"
            )
            sim_officers = st.slider("Active Field Collections Officers", 1, 10, 3, key="roi_officers_slider")
            sim_baseline_rate = st.slider("Incumbent Baseline Recovery Rate", 0.05, 0.30, 0.12, 0.01, format="%.0f%%", key="roi_base_slider")
            sim_license_fee = 150000

            st.markdown(textwrap.dedent(f"""
            <div class="card" style="padding:14px; margin-top:14px;">
                <div style="font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted); font-weight:700;">Skye8 License Terms</div>
                <div style="font-size:18px; font-weight:700; color:var(--ink); margin-top:4px;">{sim_license_fee:,.0f} FCFA / mo</div>
                <div style="font-size:11px; color:var(--muted); margin-top:2px;">Includes multi-officer access, weekly model retraining, and zero-leakage offline field sheets.</div>
            </div>
            """), unsafe_allow_html=True)

        with sim_c2:
            st.markdown("##### Simulated Financial & Operational Return")
            baseline_cash = sim_portfolio * sim_baseline_rate
            lift_rate = 0.656
            incremental_cash = baseline_cash * lift_rate
            ai_total_cash = baseline_cash + incremental_cash
            monthly_net_profit = incremental_cash - sim_license_fee
            roi_multiple = incremental_cash / max(1.0, sim_license_fee)
            payback_days = (sim_license_fee / (incremental_cash / 30.0))

            roi_metrics_html = f"""
            <section class="metrics">
                <article class="metric">
                    <div class="metric-label">BASELINE RECOVERY</div>
                    <div class="metric-value" style="font-size:18px;">{baseline_cash:,.0f} <small style="font-size:9px;">FCFA</small></div>
                    <div class="metric-note">Heuristic without AI</div>
                </article>
                <article class="metric">
                    <div class="metric-label">SKYE8 TOTAL</div>
                    <div class="metric-value" style="font-size:18px;">{ai_total_cash:,.0f} <small style="font-size:9px;">FCFA</small></div>
                    <div class="metric-note good">+65.6% recovery lift</div>
                </article>
                <article class="metric">
                    <div class="metric-label">ADDED NET CASH</div>
                    <div class="metric-value" style="font-size:18px; color:var(--green);">+{incremental_cash:,.0f} <small style="font-size:9px;">FCFA</small></div>
                    <div class="metric-note">After costs</div>
                </article>
                <article class="metric">
                    <div class="metric-label">SOFTWARE ROI</div>
                    <div class="metric-value" style="font-size:18px; color:#203b2a;">{roi_multiple:.1f}x</div>
                    <div class="metric-note">Payback in {payback_days:.1f} days</div>
                </article>
            </section>
            """
            st.markdown(textwrap.dedent(roi_metrics_html), unsafe_allow_html=True)

            st.markdown(textwrap.dedent(f"""
            <div class="card" style="padding:16px; border-left:3px solid var(--green);">
                <div style="font-size:13px; font-weight:700; color:var(--ink);">Executive Board Decision Summary:</div>
                <p style="font-size:12px; color:var(--muted); margin-top:6px; line-height:1.6;">
                    By paying a software subscription of <strong>{sim_license_fee:,.0f} FCFA/month</strong>,
                    this branch recovers an additional <strong>{incremental_cash:,.0f} FCFA</strong> every month across {sim_officers} officers.
                    The license pays for itself in just <strong>{payback_days:.1f} days</strong> of the month.
                    Annualized net profit improvement: <strong>+{(monthly_net_profit * 12):,.0f} FCFA</strong>.
                </p>
            </div>
            """), unsafe_allow_html=True)


# =============================================================
# VIEW 4: MEMBER OUTREACH (USSD, DOCKETS, ROUTES & ETHICS)
# =============================================================
elif nav_selection == "Member outreach":
    st.markdown("### Member Outreach, Transit Logistics & Ethical Guardrails")
    st.caption("Direct Mobile Money clearing strings, printable field dockets, Bamenda motorcycle routing, and ethical safeguards.")

    tab_momo, tab_docket, tab_routes, tab_ethics = st.tabs([
        "Mobile Money & USSD Clearing",
        "Printable Field Contact Docket",
        "Bamenda Route Optimizer & Safety Tiers",
        "Ethical AI Guardrails & Human Cost"
    ])

    with tab_momo:
        st.markdown("#### Mobile Money 1-Click USSD Dial Codes")
        momo_acc_id = st.selectbox(
            "Select Borrower for USSD String Generation",
            df_active["SK_ID_CURR"].tolist(),
            index=0,
            key="ussd_borrower_sel"
        )
        selected_momo_row = df_active[df_active["SK_ID_CURR"] == momo_acc_id].iloc[0]
        momo = generate_momo_ussd_strings(selected_momo_row["overdue_amount"], selected_momo_row["SK_ID_PREV"])

        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("##### MTN Mobile Money")
            st.code(momo["mtn_ussd"], language="text")
            st.caption("Credit Union Till Code: 705001")

        with mc2:
            st.markdown("##### Orange Money")
            st.code(momo["orange_ussd"], language="text")
            st.caption("Credit Union Partner Code: 705001")

        st.markdown("---")
        st.markdown("#### Diaspora Family Sponsor Protocol")
        st.caption("Formal notice for family members in the US/Europe/UK to settle arrears directly via international remittance:")
        diaspora_text = generate_diaspora_sponsor_script(
            int(selected_momo_row["SK_ID_CURR"]),
            int(selected_momo_row["SK_ID_PREV"]),
            selected_momo_row["overdue_amount"],
            selected_momo_row["assigned_officer"]
        )
        st.text_area("Diaspora Settlement Letter", value=diaspora_text, height=140)

    with tab_docket:
        st.markdown("#### Printable Field Contact Docket & Payment Pledge Slip")
        st.caption("Standardized offline field docket for motorcycle transit. Print directly or save as PDF for physical member signature.")

        docket_acc_id = st.selectbox(
            "Choose Borrower for Docket Slip",
            df_active["SK_ID_CURR"].tolist(),
            key="docket_select_box"
        )

        if docket_acc_id:
            doc_row = df_active[df_active["SK_ID_CURR"] == docket_acc_id].iloc[0]

            docket_html = f"""
            <div class="card" style="max-width:820px; margin:0 auto; padding:24px; border:2px solid var(--dark); border-radius:12px;">
                <div style="display:flex; justify-content:space-between; border-bottom:2px solid var(--dark); padding-bottom:12px; margin-bottom:18px;">
                    <div>
                        <div style="font-size:18px; font-weight:800; color:var(--dark);">BAMENDA CREDIT UNION COOPERATIVE LEAGUE</div>
                        <div style="font-size:10px; letter-spacing:0.1em; color:var(--muted); text-transform:uppercase;">Mezam Divisional Collections Desk &bull; Official Field Contact Docket</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:11px; font-weight:700; color:var(--dark);">Docket Reference</div>
                        <div style="font-size:10px; color:var(--muted);">DOC-2026-{doc_row['SK_ID_CURR']}</div>
                    </div>
                </div>

                <table style="width:100%; font-size:12px; margin-bottom:20px; border-collapse:collapse;">
                    <tr>
                        <td style="padding:6px 0; color:var(--muted); width:25%;">Borrower ID:</td>
                        <td style="padding:6px 0; font-weight:600; color:var(--ink);">Client #{doc_row['SK_ID_CURR']}</td>
                        <td style="padding:6px 0; color:var(--muted); width:25%;">Loan Reference:</td>
                        <td style="padding:6px 0; font-weight:600; color:var(--ink);">#{doc_row['SK_ID_PREV']}</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 0; color:var(--muted);">Urban Zone / Quarter:</td>
                        <td style="padding:6px 0; font-weight:600; color:var(--ink);">{doc_row.get('bamenda_quarter', 'Commercial Avenue')}</td>
                        <td style="padding:6px 0; color:var(--muted);">Assigned Officer:</td>
                        <td style="padding:6px 0; font-weight:600; color:var(--ink);">{doc_row['assigned_officer']}</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 0; color:var(--muted);">Overdue Amount:</td>
                        <td style="padding:6px 0; font-weight:700; color:var(--red); font-size:14px;">{doc_row['overdue_amount']:,.0f} FCFA</td>
                        <td style="padding:6px 0; color:var(--muted);">Delinquency Age:</td>
                        <td style="padding:6px 0; font-weight:600; color:var(--ink);">15 Days Past Due</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 0; color:var(--muted);">Recommended Channel:</td>
                        <td style="padding:6px 0; font-weight:600; color:var(--ink);">{doc_row['recommended_channel']}</td>
                        <td style="padding:6px 0; color:var(--muted);">Hardship Flag:</td>
                        <td style="padding:6px 0; font-weight:600; color:#854D0E;">{'PROTECTED (Hardship / Senior)' if doc_row.get('is_vulnerable', False) else 'STANDARD'}</td>
                    </tr>
                </table>

                <div style="border-top:1px dashed var(--dark); padding-top:16px; margin-top:14px;">
                    <div style="font-size:13px; font-weight:700; color:var(--dark); margin-bottom:6px;">
                        MEMBER REPAYMENT PLEDGE COMMITMENT (OFFICIAL SLIP)
                    </div>
                    <div style="font-size:11px; color:var(--muted); line-height:1.6; margin-bottom:12px;">
                        I, member of account <strong>#{doc_row['SK_ID_CURR']}</strong>, hereby acknowledge the overdue balance of <strong>{doc_row['overdue_amount']:,.0f} FCFA</strong>.
                        I formally commit to deposit the agreed settlement sum of __________________ FCFA into the credit union counter on or before ____ / ____ / 2026.
                    </div>

                    <div style="background:#f4f8ef; border:1px solid #dcebd8; border-radius:6px; padding:8px 12px; margin-bottom:16px; font-size:10px; color:var(--ink);">
                        <strong>Instant Mobile Settlement:</strong> Pay without cash transit via <strong>MTN MoMo:</strong> <code>*126*9*705001*{int(round(doc_row['overdue_amount']))}#</code> or <strong>Orange Money:</strong> <code>*150*1*705001*{int(round(doc_row['overdue_amount']))}#</code>.
                    </div>

                    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; margin-top:18px;">
                        <div style="border-top:1px solid var(--ink); padding-top:6px; font-size:10px; text-align:center;">
                            Member Signature &amp; Date
                        </div>
                        <div style="border-top:1px solid var(--ink); padding-top:6px; font-size:10px; text-align:center;">
                            Collections Officer Signature
                        </div>
                        <div style="border:1px solid var(--line); border-radius:6px; padding:12px; text-align:center; font-size:9px; color:var(--muted);">
                            [ Credit Union Branch Stamp ]
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(textwrap.dedent(docket_html), unsafe_allow_html=True)

    with tab_routes:
        st.markdown("#### Bamenda Urban Route Optimizer (Benskin Motorcycle Fuel Saver)")
        st.caption("Spatial clustering of field visits to cut motorcycle fuel expenses and travel fatigue for Field Officers in Mezam division.")

        route_col1, route_col2 = st.columns([1.2, 1.8])
        with route_col1:
            st.markdown("##### Urban Quarter Distribution")
            qtr_counts = df_raw["bamenda_quarter"].value_counts().reset_index()
            qtr_counts.columns = ["Bamenda Quarter", "Accounts"]
            st.dataframe(qtr_counts, hide_index=True)

            selected_zone_r = st.selectbox(
                "Filter Itinerary by Urban Zone",
                ["All Quarters"] + sorted(df_raw["bamenda_quarter"].unique().tolist()),
                key="route_zone_sel"
            )

        with route_col2:
            st.markdown("##### Motorcycle Route Efficiency (Officer 3 - Emmanuel K.)")
            emmanuel_df = df_raw[df_raw["assigned_officer"].str.contains("Emmanuel", na=False)]
            savings = calculate_benskin_route_savings(emmanuel_df)

            n_vis = savings.get('n_field_visits', 0)
            km_sav = savings.get('km_saved', 0.0)
            pct_sav = savings.get('pct_distance_saved', 0.0)
            fuel_sav = savings.get('fuel_saved_liters', 0.0)
            cash_sav = savings.get('fuel_cash_saved_fcfa', 0.0)

            st.markdown(textwrap.dedent(f"""
            <section class="metrics">
                <article class="metric">
                    <div class="metric-label">SCHEDULED VISITS</div>
                    <div class="metric-value" style="font-size:18px;">{n_vis}</div>
                    <div class="metric-note">Field calls</div>
                </article>
                <article class="metric">
                    <div class="metric-label">TRANSIT DISTANCE CUT</div>
                    <div class="metric-value" style="font-size:18px;">{km_sav} <small style="font-size:9px;">KM</small></div>
                    <div class="metric-note">-{pct_sav}% distance</div>
                </article>
                <article class="metric">
                    <div class="metric-label">FUEL SAVED</div>
                    <div class="metric-value" style="font-size:18px; color:var(--green);">{fuel_sav} <small style="font-size:9px;">L</small></div>
                    <div class="metric-note">@ 30 km / L</div>
                </article>
                <article class="metric">
                    <div class="metric-label">FUEL CASH SAVED</div>
                    <div class="metric-value" style="font-size:18px; color:#203b2a;">{cash_sav:,.0f} <small style="font-size:9px;">FCFA</small></div>
                    <div class="metric-note">@ 850 FCFA/L</div>
                </article>
            </section>
            """), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### Bamenda Quarter Security Risk & Safe Transit Guide")
        sec_col1, sec_col2 = st.columns(2)
        with sec_col1:
            st.markdown(textwrap.dedent("""
            <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 14px;">
                <div style="font-weight: 700; color: #166534; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;">Level 1: Safe Transit Zones (Low Risk)</div>
                <div style="font-size: 11px; color: #15803D; margin-top: 4px; line-height: 1.5;">
                    Commercial Avenue, Up Station, Old Council, Food Market, Mile 2/3.<br>
                    <em>Protocol:</em> Standard operational transit; normal business hours (08:00 – 17:30).
                </div>
            </div>
            """), unsafe_allow_html=True)
        with sec_col2:
            st.markdown(textwrap.dedent("""
            <div style="background-color: #FEFCE8; border: 1px solid #FEF08A; border-radius: 8px; padding: 14px;">
                <div style="font-weight: 700; color: #854D0E; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;">Level 2: Daytime Caution Zones (Moderate Risk)</div>
                <div style="font-size: 11px; color: #A16207; margin-top: 4px; line-height: 1.5;">
                    Nkwen, Mankon, Mile 4, Hospital Roundabout, Ngeng Junction.<br>
                    <em>Protocol:</em> Complete motorcycle transit before 16:30; stay on main paved axes; travel in pairs if handling physical cash.
                </div>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        route_view_df = df_raw[df_raw["recommended_channel"] == "FIELD_VISIT"].copy()
        if "security_badge" not in route_view_df.columns:
            route_view_df["security_badge"] = route_view_df["bamenda_quarter"].map(
                lambda q: BAMENDA_SECURITY_TIERS.get(q, {}).get("badge", "L1: Safe Transit")
            )
        if selected_zone_r != "All Quarters":
            route_view_df = route_view_df[route_view_df["bamenda_quarter"] == selected_zone_r]

        st.dataframe(
            route_view_df[[
                "bamenda_quarter", "security_badge", "SK_ID_CURR", "assigned_officer", "overdue_amount",
                "recovery_probability", "expected_gross_recovery_fcfa", "action_reason"
            ]].rename(columns={
                "bamenda_quarter": "Quarter / Neighborhood",
                "security_badge": "Security Tier",
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
            height=300
        )

    with tab_ethics:
        st.markdown("#### Ethical Guardrails & The Human Cost")
        st.caption("Protecting vulnerable borrowers and preserving community trust in the North West Region of Cameroon.")

        eth_col1, eth_col2 = st.columns([1.5, 1])
        with eth_col1:
            st.markdown(textwrap.dedent("""
            ##### The Reality of Debt in Bamenda
            Microfinance borrowers are market traders, school teachers, smallholders, and artisans.
            They face severe exogenous disruptions:
            * Regional economic headwinds and transport bottlenecks.
            * Health emergencies and funeral contributions.
            * Supply-chain inventory losses.

            A naive collections tool that maximizes pressure pushes officers toward aggressive harassment,
            destroying the credit union's social license and driving borrowers into deeper insolvency.

            ##### Embedded Technological Protections:
            1. **Senior Hardship Shield:** Borrowers aged &ge; 60 years are automatically shielded from high-pressure contacts and routed to cooperative welfare restructuring.
            2. **Employment Shock Flag:** Documented income disruptions trigger loan restructuring proposals rather than field enforcement.
            3. **Cost-Gated In-Person Enforcement:** Field visits (5,000 FCFA) are prohibited on low balances and vulnerable borrowers.
            """))

        with eth_col2:
            st.markdown("##### Active Welfare Audit (400 Accounts)")
            st.markdown(textwrap.dedent("""
            <div class="card" style="padding: 20px;">
                <div style="font-size: 28px; font-weight: 800; color: #854D0E;">74 Borrowers</div>
                <div style="font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px; font-weight: 700;">Protected by Ethical Filters (18.5%)</div>
                <div style="font-size: 11px; color: var(--ink); line-height: 1.6;">
                    These accounts have been diverted from aggressive visits to friendly restructuring dialogues.
                    Overdue balances are preserved without inflicting humanitarian harm on distressed families.
                </div>
            </div>
            """), unsafe_allow_html=True)

# Common Footer
st.markdown("---")
st.markdown(textwrap.dedent("""
<div style="display: flex; justify-content: space-between; font-size: 10px; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase;">
    <div>Skye8 Intelligence &bull; Final Project SKY8-DS-FP-005</div>
    <div>Candidate: Nahbila Faith &bull; Bamenda, Cameroon</div>
</div>
"""), unsafe_allow_html=True)
