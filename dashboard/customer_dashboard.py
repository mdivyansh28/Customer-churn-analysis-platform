import streamlit as st
import pandas as pd
import plotly.express as px
from src.customer_analysis import CustomerAnalytics


def _inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    :root {
        --bg:#0a0c10; --surface:#111318; --border:#1e2230;
        --accent:#4f8ef7; --accent2:#00e5c3; --danger:#f75757;
        --text:#e8eaf0; --muted:#6b7280;
    }
    html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;font-family:'DM Sans',sans-serif;color:var(--text);}
    [data-testid="stSidebar"]{background:#0d0f14!important;border-right:1px solid var(--border);}
    [data-testid="stHeader"]{background:transparent!important;}
    #MainMenu,footer,header{visibility:hidden;}
    .block-container{padding:2.5rem 3rem 4rem!important;max-width:1200px;}
    h1,h2,h3{font-family:'Syne',sans-serif!important;}
    .page-header{display:flex;align-items:center;gap:1rem;padding-bottom:1.4rem;border-bottom:1px solid var(--border);margin-bottom:2rem;}
    .page-icon{width:48px;height:48px;background:linear-gradient(135deg,#1a2a4a,#0d1829);border:1px solid #2a3a5a;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 0 18px rgba(79,142,247,.2);}
    .page-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#e8eaf0 0%,#4f8ef7 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;letter-spacing:-.4px;}
    .page-subtitle{color:var(--muted);font-size:.82rem;margin:0;}
    .section-label{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:1rem;padding-top:.2rem;}
    </style>
    """, unsafe_allow_html=True)


def show_customer_dashboard():

    _inject_styles()

    st.markdown("""
    <div class="page-header">
        <div class="page-icon">👤</div>
        <div>
            <p class="page-title">Customer Analytics</p>
            <p class="page-subtitle">Demographic breakdown &amp; segment behaviour</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = pd.read_csv("data/Customer Churn.csv")

    st.sidebar.markdown(
        "<p style='font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;"
        "color:#6b7280;margin-bottom:.5rem'>Filter — Gender</p>",
        unsafe_allow_html=True,
    )
    gender_filter = st.sidebar.multiselect(
        "",
        df["gender"].unique(),
        default=df["gender"].unique(),
        label_visibility="collapsed",
    )
    df = df[df["gender"].isin(gender_filter)]

    analytics = CustomerAnalytics(df)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-label">Gender Distribution</p>', unsafe_allow_html=True)
        gender_df = analytics.gender_distribution()
        fig = px.pie(
            gender_df, values="count", names="gender",
            color_discrete_sequence=["#4f8ef7", "#00e5c3"],
            hole=0.42,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0", legend=dict(font_size=12),
            margin=dict(t=10, b=10, l=10, r=10),
        )
        fig.update_traces(textfont_size=13, textfont_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-label">Senior Citizen Breakdown</p>', unsafe_allow_html=True)
        senior_df = analytics.senior_citizen_analysis()
        fig2 = px.bar(
            senior_df, x="SeniorCitizen", y="Count",
            color_discrete_sequence=["#4f8ef7"],
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0", xaxis=dict(gridcolor="#1e2230"),
            yaxis=dict(gridcolor="#1e2230"),
            margin=dict(t=10, b=40, l=40, r=10),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-label">Contract Analysis</p>', unsafe_allow_html=True)
    contract_df = analytics.contract_analysis()
    st.dataframe(contract_df, use_container_width=True, hide_index=True)
    st.download_button(
        label="↓  Export as CSV",
        data=contract_df.to_csv(index=False),
        file_name="customer_analysis.csv",
        mime="text/csv",
    )