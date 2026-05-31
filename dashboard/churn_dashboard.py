import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from src.churn_analysis import ChurnAnalytics


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
    .page-icon{width:48px;height:48px;background:linear-gradient(135deg,#2a1a3a,#180d29);border:1px solid #3a2a5a;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 0 18px rgba(180,80,247,.18);}
    .page-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#e8eaf0 0%,#b450f7 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;letter-spacing:-.4px;}
    .page-subtitle{color:var(--muted);font-size:.82rem;margin:0;}
    .section-label{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:.8rem;padding-top:.2rem;}
    </style>
    """, unsafe_allow_html=True)


def show_churn_dashboard():

    _inject_styles()

    st.markdown("""
    <div class="page-header">
        <div class="page-icon">⚡</div>
        <div>
            <p class="page-title">Churn Analytics</p>
            <p class="page-subtitle">Contract, gender &amp; correlation deep-dives</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = pd.read_csv("data/Customer Churn.csv")
    analytics = ChurnAnalytics(df)

    PURPLE = ["#b450f7", "#4f8ef7"]

    # ── Churn by Contract ─────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Churn by Contract Type</p>', unsafe_allow_html=True)
    contract = analytics.churn_by_contract()
    fig = px.bar(
        contract, barmode="group",
        color_discrete_sequence=PURPLE,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8eaf0", xaxis=dict(gridcolor="#1e2230"),
        yaxis=dict(gridcolor="#1e2230"), legend=dict(font_size=12),
        margin=dict(t=10, b=40, l=40, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Churn by Gender ───────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Churn by Gender</p>', unsafe_allow_html=True)
    gender = analytics.churn_by_gender()
    fig2 = px.bar(
        gender, barmode="group",
        color_discrete_sequence=PURPLE,
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8eaf0", xaxis=dict(gridcolor="#1e2230"),
        yaxis=dict(gridcolor="#1e2230"), legend=dict(font_size=12),
        margin=dict(t=10, b=40, l=40, r=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Correlation Heatmap ───────────────────────────────────────────────────
    st.markdown('<p class="section-label">Feature Correlation Matrix</p>', unsafe_allow_html=True)
    corr = analytics.correlation_matrix()

    fig3, ax = plt.subplots(figsize=(9, 5))
    fig3.patch.set_facecolor("#111318")
    ax.set_facecolor("#111318")

    sns.heatmap(
        corr, annot=True, fmt=".2f",
        cmap=sns.diverging_palette(250, 320, s=80, l=45, as_cmap=True),
        linewidths=.4, linecolor="#1e2230",
        annot_kws={"size": 8, "color": "#e8eaf0"},
        ax=ax,
    )
    ax.tick_params(colors="#6b7280", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e2230")
    plt.tight_layout()
    st.pyplot(fig3)
