"""Skyes Intelligence — Recovery Decision Workspace.

Production server serving the exact pixel-perfect ux.html layout with 100% feature preservation:
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
import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Skyes Intelligence — Account review",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Completely hide Streamlit default chrome so only the exact ux.html design renders
st.markdown("""
<style>
    /* Hide Streamlit Header, Footer, and Toolbar */
    header[data-testid="stHeader"], footer, #MainMenu { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    
    /* Strip default padding and margins */
    .main { 
        overflow: hidden !important; 
        background: transparent !important; 
        padding: 0 !important;
    }
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        margin: 0 !important;
    }
    
    /* Full-viewport seamless iframe without border */
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

HTML_FILE = Path(__file__).resolve().parent / "index.html"
if HTML_FILE.exists():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=1950, scrolling=True)
else:
    st.error("app/index.html not found.")
