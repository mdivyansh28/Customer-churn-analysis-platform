import streamlit as st
import pandas as pd
from src.customer_analysis import CustomerAnalytics


def show_home():

    # ── Inject global styles ──────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Root palette ── */
    :root {
        --bg:        #0a0c10;
        --surface:   #111318;
        --border:    #1e2230;
        --accent:    #4f8ef7;
        --accent2:   #00e5c3;
        --danger:    #f75757;
        --text:      #e8eaf0;
        --muted:     #6b7280;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }
    [data-testid="stSidebar"] { background: #0d0f14 !important; border-right: 1px solid var(--border); }
    [data-testid="stHeader"]  { background: transparent !important; }

    /* hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    .block-container { padding: 2.5rem 3rem 4rem !important; max-width: 1200px; }

    h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

    /* ── Hero banner ── */
    .hero {
        display: flex;
        align-items: center;
        gap: 1.4rem;
        padding: 2.4rem 2.8rem;
        background: linear-gradient(135deg, #111827 0%, #0f1623 60%, #0a1020 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 260px; height: 260px;
        background: radial-gradient(circle, rgba(79,142,247,.18) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-icon {
        width: 64px; height: 64px;
        background: linear-gradient(135deg, #1a2a4a, #0d1829);
        border: 1px solid #2a3a5a;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem;
        flex-shrink: 0;
        box-shadow: 0 0 24px rgba(79,142,247,.25);
    }
    .hero-text h1 {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e8eaf0 0%, #4f8ef7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 .3rem;
        letter-spacing: -0.5px;
    }
    .hero-text p {
        color: var(--muted);
        margin: 0;
        font-size: .9rem;
        font-weight: 300;
    }

    /* ── KPI cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        position: relative;
        overflow: hidden;
        transition: border-color .2s;
    }
    .kpi-card:hover { border-color: #2e3a5a; }
    .kpi-card .label {
        font-size: .72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--muted);
        margin-bottom: .5rem;
    }
    .kpi-card .value {
        font-family: 'Syne', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1;
    }
    .kpi-card .accent-bar {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
    }
    .kpi-card.blue  .accent-bar { background: linear-gradient(90deg, var(--accent), transparent); }
    .kpi-card.teal  .accent-bar { background: linear-gradient(90deg, var(--accent2), transparent); }
    .kpi-card.red   .accent-bar { background: linear-gradient(90deg, var(--danger), transparent); }
    .kpi-card.teal .value { color: var(--accent2); }
    .kpi-card.red  .value { color: var(--danger); }

    /* ── Overview section ── */
    .overview-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
    }
    .overview-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.6rem 2rem;
    }
    .overview-card h3 {
        font-size: .75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--muted);
        margin-bottom: 1.2rem;
    }
    .module-list { list-style: none; padding: 0; margin: 0; }
    .module-list li {
        display: flex;
        align-items: center;
        gap: .75rem;
        padding: .55rem 0;
        border-bottom: 1px solid var(--border);
        font-size: .9rem;
        color: #c0c8d8;
    }
    .module-list li:last-child { border-bottom: none; }
    .module-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--accent);
        flex-shrink: 0;
    }
    .stack-badge {
        display: inline-block;
        background: #161c2a;
        border: 1px solid #2a3450;
        border-radius: 6px;
        padding: .3rem .75rem;
        font-size: .78rem;
        color: #8fa8d0;
        margin: .25rem .2rem;
    }
    .section-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.8rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Data ──────────────────────────────────────────────────────────────────
    df = pd.read_csv("data/Customer Churn.csv")
    analytics = CustomerAnalytics(df)

    total    = analytics.total_customers()
    active   = analytics.active_customers()
    churned  = analytics.churned_customers()
    ret_rate = analytics.retention_rate()
    churn_rt = analytics.churn_rate()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-icon">◈</div>
        <div class="hero-text">
            <h1>Churn Intelligence Platform</h1>
            <p>Customer retention analytics &amp; risk scoring engine</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI strip ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="label">Total Customers</div>
            <div class="value">{total:,}</div>
            <div class="accent-bar"></div>
        </div>
        <div class="kpi-card blue">
            <div class="label">Active Customers</div>
            <div class="value">{active:,}</div>
            <div class="accent-bar"></div>
        </div>
        <div class="kpi-card red">
            <div class="label">Churned Customers</div>
            <div class="value">{churned:,}</div>
            <div class="accent-bar"></div>
        </div>
        <div class="kpi-card teal">
            <div class="label">Retention Rate</div>
            <div class="value">{ret_rate}%</div>
            <div class="accent-bar"></div>
        </div>
        <div class="kpi-card red">
            <div class="label">Churn Rate</div>
            <div class="value">{churn_rt}%</div>
            <div class="accent-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Overview ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="overview-section">
        <div class="overview-card">
            <h3>Platform Modules</h3>
            <ul class="module-list">
                <li><span class="module-dot"></span>Customer Analytics</li>
                <li><span class="module-dot"></span>Churn Analytics</li>
                <li><span class="module-dot"></span>Revenue Analytics</li>
                <li><span class="module-dot"></span>Customer Risk Prediction</li>
                <li><span class="module-dot"></span>Retention Recommendations</li>
            </ul>
        </div>
        <div class="overview-card">
            <h3>Tech Stack</h3>
            <div style="padding-top:.3rem">
                <span class="stack-badge">Python</span>
                <span class="stack-badge">Streamlit</span>
                <span class="stack-badge">scikit-learn</span>
                <span class="stack-badge">Plotly</span>
                <span class="stack-badge">Pandas</span>
                <span class="stack-badge">Power BI</span>
                <span class="stack-badge">Machine Learning</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
