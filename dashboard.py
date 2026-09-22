import threading
import requests
import time

def keep_alive():
    while True:
        time.sleep(14 * 60)  # 14 minutes
        try:
            requests.get("https://fintech-credit-risk-dashboard.streamlit.app/")
        except:
            pass

thread = threading.Thread(target=keep_alive, daemon=True)
thread.start()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Credit Risk Intelligence | LendingClub Analysis", page_icon="◆", layout="wide")

# ---------------------------------------------------------------------------
# DESIGN SYSTEM
# ---------------------------------------------------------------------------
NAVY = "#06070C"
PANEL = "#111220"
SLATE = "#3B82F6"
TEAL = "#22C79A"
CORAL = "#F0A93C"
PURPLE = "#6C5CE7"
TEXT = "#F2F3F7"
MUTED = "#84869C"
BORDER = "#1E1F2E"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {NAVY};
    color: {TEXT};
}}
h1, h2, h3, .hero-title {{
    font-family: 'Space Grotesk', sans-serif !important;
}}
[data-testid="stAppViewContainer"] {{ background-color: {NAVY}; }}
[data-testid="stSidebar"] {{ background-color: {PANEL}; border-right: 1px solid {BORDER}; }}
[data-testid="stHeader"] {{ background-color: transparent; }}
#MainMenu {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

.topbar-brand {{
    color: {TEXT};
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
    padding-top: 4px;
}}

.block-container {{
    padding-top: 0.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
}}

.hero {{
    padding: 26px 32px;
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 16px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}}
.hero::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {PURPLE}, {SLATE}, {TEAL});
}}
.hero-eyebrow {{
    color: {PURPLE};
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 8px;
}}
.hero-title {{
    font-size: 30px;
    font-weight: 700;
    color: {TEXT};
    margin: 0 0 8px 0;
}}
.hero-sub {{
    color: {MUTED};
    font-size: 14px;
    margin: 0;
    max-width: 720px;
}}

.kpi-card {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}}
.kpi-purple::before {{ background: {PURPLE}; }}
.kpi-orange::before {{ background: {CORAL}; }}
.kpi-blue::before {{ background: {SLATE}; }}
.kpi-teal::before {{ background: {TEAL}; }}
.kpi-icon {{
    width: 36px; height: 36px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
    margin-bottom: 12px;
}}
.kpi-purple .kpi-icon {{ background: rgba(124,92,252,0.15); }}
.kpi-orange .kpi-icon {{ background: rgba(245,166,35,0.15); }}
.kpi-blue .kpi-icon {{ background: rgba(59,130,246,0.15); }}
.kpi-teal .kpi-icon {{ background: rgba(16,185,129,0.15); }}
.kpi-label {{
    color: {MUTED};
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 6px;
    font-weight: 600;
}}
.kpi-value {{
    color: {TEXT};
    font-size: 27px;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
}}

.section-label {{
    color: {PURPLE};
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
    margin: 8px 0 2px 0;
}}
.section-title {{
    color: {TEXT};
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 14px 0;
    font-family: 'Space Grotesk', sans-serif;
}}

.insight-box {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 22px;
    text-align: center;
    position: relative;
    overflow: hidden;
}}
.insight-box::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: {CORAL};
}}
.insight-value {{
    font-size: 40px;
    font-weight: 700;
    color: {CORAL};
    font-family: 'Space Grotesk', sans-serif;
}}
.insight-label {{
    color: {MUTED};
    font-size: 13px;
    margin-top: 8px;
}}

.footer-note {{
    color: {MUTED};
    font-size: 12.5px;
    border-top: 1px solid {BORDER};
    padding-top: 16px;
    margin-top: 8px;
    line-height: 1.6;
}}

[data-testid="stMetricValue"] {{ color: {TEXT}; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 8px 8px 0 0;
    color: {MUTED};
    padding: 8px 18px;
}}
.stTabs [aria-selected="true"] {{
    color: {PURPLE} !important;
    border-bottom: 2px solid {PURPLE} !important;
}}

/* Multiselect tag pills — replace default red with palette-matched style */
span[data-baseweb="tag"] {{
    background-color: rgba(124,92,252,0.18) !important;
    border: 1px solid {PURPLE} !important;
    color: {TEXT} !important;
    border-radius: 6px !important;
}}
span[data-baseweb="tag"] svg {{ fill: {TEXT} !important; }}
[data-testid="stMultiSelect"] > div > div {{
    background-color: {NAVY} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
}}
[data-testid="stMultiSelect"] label p {{
    color: {MUTED} !important;
    font-size: 12.5px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* Filters popover button */
[data-testid="stPopover"] button {{
    background-color: {PANEL} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}}
[data-testid="stPopover"] button:hover {{
    border-color: {PURPLE} !important;
    color: {PURPLE} !important;
}}
.block-container {{
    padding-bottom: 1rem !important;
}}

</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Inter"),
        title_font=dict(family="Space Grotesk", size=15, color=TEXT),
        colorway=[PURPLE, TEAL, CORAL, SLATE, "#A78BFA", "#F2986E"],
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        margin=dict(t=50, l=10, r=10, b=10),
    )
)

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('loans_export.csv')
    df['issue_d'] = pd.to_datetime(df['issue_d'], errors='coerce')
    bins = [0, 10, 20, 30, 100]
    labels = ['0-10', '10-20', '20-30', '30+']
    df['dti_bucket'] = pd.cut(df['dti'], bins=bins, labels=labels)
    income_bins = [0, 30000, 60000, 100000, float('inf')]
    income_labels = ['Low (<30K)', 'Mid (30-60K)', 'High (60-100K)', 'Very High (100K+)']
    df['income_bucket'] = pd.cut(df['annual_inc'], bins=income_bins, labels=income_labels)
    return df

df = load_data()

# ---------------------------------------------------------------------------
# TOP BAR — brand + filters (replaces default Streamlit Deploy button area)
# ---------------------------------------------------------------------------
top_left, top_right = st.columns([5, 1])
with top_left:
    st.markdown('<div class="topbar-brand">Ritesh\'s Analysis</div>', unsafe_allow_html=True)
with top_right:
    with st.popover("⚙️ Filters", use_container_width=True):
        grade_filter = st.multiselect("Grade", sorted(df['grade'].unique()), default=sorted(df['grade'].unique()))
        term_filter = st.multiselect("Term", df['term'].unique(), default=df['term'].unique())
        purpose_filter = st.multiselect("Purpose", sorted(df['purpose'].unique()), default=sorted(df['purpose'].unique()))

filtered = df[
    df['grade'].isin(grade_filter) &
    df['term'].isin(term_filter) &
    df['purpose'].isin(purpose_filter)
]

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Credit Risk Analytics · Fintech Case Study</div>
    <div class="hero-title">Why Data Analysis Wins: Capital One vs. Wonga</div>
    <p class="hero-sub">1.37M real LendingClub loan records analyzed to reveal the risk signals that separated a
    data-driven $50B+ bank from a lender that collapsed after £220M in bad loans.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI ROW
# ---------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "purple", "📄", "Total Loans", f"{len(filtered):,}"),
    (k2, "orange", "⚠️", "Default Rate", f"{filtered['is_default'].mean()*100:.2f}%"),
    (k3, "blue", "💰", "Total Loan Volume", f"${filtered['loan_amnt'].sum()/1e9:.2f}bn"),
    (k4, "teal", "📈", "Avg Interest Rate", f"{filtered['int_rate'].mean():.2f}%"),
]
for col, tone, icon, label, value in kpis:
    col.markdown(f"""<div class="kpi-card kpi-{tone}">
    <div class="kpi-icon">{icon}</div>
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Risk Segmentation", "Affordability", "Geographic & Purpose"])

with tab1:
    st.markdown('<div class="section-label">Executive Summary</div><div class="section-title">Portfolio Risk at a Glance</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        grade_default = filtered.groupby('grade')['is_default'].mean().reset_index()
        grade_default['is_default'] *= 100
        fig = px.bar(grade_default, x='grade', y='is_default', title="Default Rate % by Credit Grade",
                     labels={'is_default': 'Default Rate %'}, template=PLOTLY_TEMPLATE)
        fig.update_traces(marker_color=PURPLE)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        trend = filtered.groupby(filtered['issue_d'].dt.to_period('M')).size().reset_index(name='count')
        trend['issue_d'] = trend['issue_d'].astype(str)
        fig2 = px.line(trend, x='issue_d', y='count', title="Loan Origination Volume Over Time", template=PLOTLY_TEMPLATE)
        fig2.update_traces(line_color=TEAL)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown('<div class="section-label">The Capital One Model</div><div class="section-title">Pricing Risk Through Segmentation</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        matrix = filtered.groupby(['grade', 'dti_bucket'], observed=True)['is_default'].mean().reset_index()
        matrix['is_default'] *= 100
        pivot = matrix.pivot(index='grade', columns='dti_bucket', values='is_default')
        fig3 = px.imshow(pivot, text_auto='.1f', title="Default Rate % — Grade × DTI Bucket",
                          color_continuous_scale=[PANEL, PURPLE, CORAL], template=PLOTLY_TEMPLATE)
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        rate_by_grade = filtered.groupby('grade')['int_rate'].mean().reset_index()
        fig4 = px.bar(rate_by_grade, x='grade', y='int_rate', title="Avg Interest Rate by Grade (Risk-Based Pricing)", template=PLOTLY_TEMPLATE)
        fig4.update_traces(marker_color=TEAL)
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.markdown('<div class="section-label">The Wonga Failure Point</div><div class="section-title">Where Weak Affordability Checks Break Down</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 0.8])
    with c1:
        dti_default = filtered.groupby('dti_bucket', observed=True)['is_default'].mean().reset_index()
        dti_default['is_default'] *= 100
        fig5 = px.bar(dti_default, x='dti_bucket', y='is_default', title="Default Rate % by DTI Bucket", template=PLOTLY_TEMPLATE)
        fig5.update_traces(marker_color=CORAL)
        st.plotly_chart(fig5, use_container_width=True)
    with c2:
        inc_default = filtered.groupby('income_bucket', observed=True)['is_default'].mean().reset_index()
        inc_default['is_default'] *= 100
        fig6 = px.bar(inc_default, x='income_bucket', y='is_default', title="Default Rate % by Income Bucket", template=PLOTLY_TEMPLATE)
        fig6.update_traces(marker_color=PURPLE)
        st.plotly_chart(fig6, use_container_width=True)
    with c3:
        high_risk = filtered[filtered['dti'] >= 30]
        rate = high_risk['is_default'].mean() * 100 if len(high_risk) > 0 else 0
        st.markdown(f"""<div class="insight-box"><div class="insight-value">{rate:.1f}%</div>
        <div class="insight-label">Default rate on loans with DTI ≥ 30 — the exact<br>affordability signal weak risk checks miss</div></div>""", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-label">Concentration Risk</div><div class="section-title">Geographic & Purpose Breakdown</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        state_default = filtered.groupby('addr_state')['is_default'].mean().reset_index()
        state_default['is_default'] *= 100
        state_default = state_default.sort_values('is_default', ascending=False)
        fig7 = px.bar(state_default, x='addr_state', y='is_default', title="Default Rate % by State", template=PLOTLY_TEMPLATE)
        fig7.update_traces(marker_color=PURPLE)
        st.plotly_chart(fig7, use_container_width=True)
    with c2:
        purpose_default = filtered.groupby('purpose')['is_default'].mean().reset_index()
        purpose_default['is_default'] *= 100
        purpose_default = purpose_default.sort_values('is_default', ascending=False)
        fig8 = px.bar(purpose_default, x='purpose', y='is_default', title="Default Rate % by Loan Purpose", template=PLOTLY_TEMPLATE)
        fig8.update_traces(marker_color=TEAL)
        st.plotly_chart(fig8, use_container_width=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="footer-note" style="margin-top:0px; padding-top:10px;">
Capital One (founded 1994) priced credit risk per borrower using data and grew into a top-10 US bank.
Wonga automated loan approvals without rigorous affordability analysis, wrote off £220M in loans (2014),
and collapsed into administration in 2018. This dashboard replicates that exact risk-decision point on
1.37M real lending records — built with Python, MySQL, and Streamlit.
</div>
""", unsafe_allow_html=True)