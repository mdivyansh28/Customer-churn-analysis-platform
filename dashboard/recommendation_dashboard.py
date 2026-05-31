import streamlit as st
from src.recommendation_engine import RecommendationEngine


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
    .page-icon{width:48px;height:48px;background:linear-gradient(135deg,#1a3a1a,#0d290d);border:1px solid #2a5a2a;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 0 18px rgba(0,229,100,.15);}
    .page-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#e8eaf0 0%,#00e564 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;letter-spacing:-.4px;}
    .page-subtitle{color:var(--muted);font-size:.82rem;margin:0;}

    .section-label{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:.8rem;}

    /* Risk level pill */
    .risk-pill{
        display:inline-flex;align-items:center;gap:.5rem;
        padding:.5rem 1.2rem;border-radius:999px;
        font-family:'Syne',sans-serif;font-weight:700;font-size:.85rem;
        margin-bottom:1.6rem;
    }
    .risk-low{background:#0d2a1f;color:#00e564;border:1px solid #0e4a30;}
    .risk-medium{background:#2a2f10;color:#d4e057;border:1px solid #4a5215;}
    .risk-high{background:#3d2710;color:#f79f57;border:1px solid #6b4215;}
    .risk-critical{background:#3d1010;color:#f75757;border:1px solid #6b1515;}

    /* Recommendation cards */
    .rec-card{
        display:flex;align-items:flex-start;gap:1rem;
        background:var(--surface);border:1px solid var(--border);
        border-left:3px solid var(--accent2);
        border-radius:10px;padding:1.1rem 1.4rem;margin-bottom:.8rem;
        transition:border-color .2s,background .2s;
    }
    .rec-card:hover{background:#151b26;border-left-color:#4f8ef7;}
    .rec-card .rec-num{
        font-family:'Syne',sans-serif;font-size:.75rem;font-weight:700;
        color:var(--accent2);min-width:24px;padding-top:.1rem;
    }
    .rec-card .rec-text{font-size:.9rem;color:#c8d4e8;line-height:1.55;}

    /* Slider label override */
    [data-testid="stSlider"] label{color:var(--muted)!important;font-size:.8rem!important;}
    </style>
    """, unsafe_allow_html=True)


def _risk_label(prob: float) -> tuple[str, str]:
    if prob >= 0.80:
        return "Critical Risk", "risk-critical"
    elif prob >= 0.60:
        return "High Risk", "risk-high"
    elif prob >= 0.40:
        return "Medium Risk", "risk-medium"
    else:
        return "Low Risk", "risk-low"


def show_recommendation_dashboard():

    _inject_styles()

    st.markdown("""
    <div class="page-header">
        <div class="page-icon">🛡</div>
        <div>
            <p class="page-title">Retention Engine</p>
            <p class="page-subtitle">AI-powered retention actions based on churn probability</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Probability slider ────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Customer Churn Probability</p>', unsafe_allow_html=True)

    probability = st.slider(
        "",
        min_value=0.0,
        max_value=1.0,
        value=0.50,
        step=0.01,
        label_visibility="collapsed",
    )

    # Risk pill
    label, css_class = _risk_label(probability)
    st.markdown(f"""
    <div class="risk-pill {css_class}">
        <span>●</span> {label} — {probability:.0%} churn probability
    </div>
    """, unsafe_allow_html=True)

    # ── Recommendations ───────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Recommended Retention Actions</p>', unsafe_allow_html=True)

    engine = RecommendationEngine()
    recommendations = engine.generate(probability)

    if recommendations:
        for i, item in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="rec-card">
                <span class="rec-num">#{i:02d}</span>
                <span class="rec-text">{item}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="color:#6b7280;font-size:.9rem;padding:1rem 0">
            No recommendations available for the selected probability range.
        </div>
        """, unsafe_allow_html=True)