import streamlit as st
import pandas as pd
import plotly.express as px
from src.revenue_analysis import RevenueAnalytics


def _inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    :root{--bg:#0a0c10;--surface:#111318;--border:#1e2230;--accent:#4f8ef7;--accent2:#00e5c3;--danger:#f75757;--text:#e8eaf0;--muted:#6b7280;}
    html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;font-family:'DM Sans',sans-serif;color:var(--text);}
    [data-testid="stSidebar"]{background:#0d0f14!important;border-right:1px solid var(--border);}
    [data-testid="stHeader"]{background:transparent!important;}
    #MainMenu,footer,header{visibility:hidden;}
    .block-container{padding:2.5rem 3rem 4rem!important;max-width:1200px;}
    h1,h2,h3{font-family:'Syne',sans-serif!important;}

    .page-header{display:flex;align-items:center;gap:1rem;padding-bottom:1.4rem;border-bottom:1px solid var(--border);margin-bottom:2rem;}
    .page-icon{width:48px;height:48px;background:linear-gradient(135deg,#1a3a2a,#0d2918);border:1px solid #2a5a3a;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 0 18px rgba(0,229,195,.15);}
    .page-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#e8eaf0 0%,#00e5c3 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;letter-spacing:-.4px;}
    .page-subtitle{color:var(--muted);font-size:.82rem;margin:0;}

    .kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem;}
    .kpi{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.4rem;position:relative;overflow:hidden;}
    .kpi:hover{border-color:#2e3a5a;}
    .kpi .lbl{font-size:.7rem;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:.4rem;}
    .kpi .val{font-family:'Syne',sans-serif;font-size:1.65rem;font-weight:700;color:var(--text);line-height:1;}
    .kpi .bar{position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent2),transparent);}
    .kpi.loss .val{color:var(--danger);}
    .kpi.loss .bar{background:linear-gradient(90deg,var(--danger),transparent);}

    .section-label{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:.8rem;padding-top:.2rem;}
    </style>
    """, unsafe_allow_html=True)


def show_revenue_dashboard():

    _inject_styles()

    st.markdown("""
    <div class="page-header">
        <div class="page-icon">$</div>
        <div>
            <p class="page-title">Revenue Analytics</p>
            <p class="page-subtitle">Revenue performance, loss exposure &amp; lifetime value</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = pd.read_csv("data/Customer Churn.csv")
    analytics = RevenueAnalytics(df)

    total_rev  = analytics.total_revenue()
    rev_loss   = analytics.revenue_loss()
    arpu       = analytics.arpu()
    clv        = analytics.customer_lifetime_value()

    # ── KPI row ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi">
            <div class="lbl">Total Revenue</div>
            <div class="val">${total_rev:,.0f}</div>
            <div class="bar"></div>
        </div>
        <div class="kpi loss">
            <div class="lbl">Revenue at Risk</div>
            <div class="val">${rev_loss:,.0f}</div>
            <div class="bar"></div>
        </div>
        <div class="kpi">
            <div class="lbl">ARPU</div>
            <div class="val">{arpu}</div>
            <div class="bar"></div>
        </div>
        <div class="kpi">
            <div class="lbl">CLV</div>
            <div class="val">{clv}</div>
            <div class="bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    TEAL = ["#00e5c3"]

    # ── Revenue by Contract ───────────────────────────────────────────────────
    st.markdown('<p class="section-label">Revenue by Contract Type</p>', unsafe_allow_html=True)
    contract_df = analytics.revenue_by_contract()
    fig = px.bar(
        contract_df, x="Contract", y="MonthlyCharges",
        color_discrete_sequence=TEAL,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8eaf0", xaxis=dict(gridcolor="#1e2230"),
        yaxis=dict(gridcolor="#1e2230"),
        margin=dict(t=10, b=40, l=40, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Revenue Forecast ──────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Revenue Forecast</p>', unsafe_allow_html=True)
    forecast = analytics.revenue_forecast()
    fig2 = px.line(
        forecast, x="Month", y="ForecastRevenue",
        color_discrete_sequence=TEAL,
        markers=True,
    )
    fig2.update_traces(line_width=2.5, marker_size=6)
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8eaf0", xaxis=dict(gridcolor="#1e2230"),
        yaxis=dict(gridcolor="#1e2230"),
        margin=dict(t=10, b=40, l=40, r=10),
    )
    st.plotly_chart(fig2, use_container_width=True)
