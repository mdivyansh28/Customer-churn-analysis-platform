import streamlit as st
import pandas as pd
import joblib


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
    .page-icon{width:48px;height:48px;background:linear-gradient(135deg,#2a1a1a,#291010);border:1px solid #5a2a2a;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 0 18px rgba(247,87,87,.18);}
    .page-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#e8eaf0 0%,#f75757 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;letter-spacing:-.4px;}
    .page-subtitle{color:var(--muted);font-size:.82rem;margin:0;}

    /* Upload zone */
    .upload-hint{
        background:var(--surface);border:1px dashed #2e3a5a;border-radius:12px;
        padding:2.4rem;text-align:center;color:var(--muted);font-size:.9rem;
        margin-bottom:1.5rem;
    }
    .upload-hint .icon{font-size:2rem;margin-bottom:.6rem;}
    .upload-hint strong{color:#8fa8d0;font-weight:500;}

    /* Risk badges */
    .badge{display:inline-block;padding:.2rem .65rem;border-radius:5px;font-size:.72rem;font-weight:600;letter-spacing:.5px;}
    .badge-critical{background:#3d1010;color:#f75757;border:1px solid #6b1515;}
    .badge-high{background:#3d2710;color:#f79f57;border:1px solid #6b4215;}
    .badge-medium{background:#2a2f10;color:#d4e057;border:1px solid #4a5215;}
    .badge-low{background:#0d2a1f;color:#00e5c3;border:1px solid #0e4a35;}

    .section-label{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:.8rem;}

    /* Streamlit file uploader tweak */
    [data-testid="stFileUploader"]{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;}
    </style>
    """, unsafe_allow_html=True)


def show_prediction_dashboard():

    _inject_styles()

    st.markdown("""
    <div class="page-header">
        <div class="page-icon">🎯</div>
        <div>
            <p class="page-title">Customer Risk Prediction</p>
            <p class="page-subtitle">Upload customer data to score churn probability &amp; risk bucket</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload zone ───────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Upload Customer CSV</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop a CSV file here, or click to browse",
        type=["csv"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.markdown("""
        <div class="upload-hint">
            <div class="icon">📂</div>
            <div>Drag &amp; drop a <strong>.csv</strong> file or use the uploader above</div>
            <div style="margin-top:.4rem;font-size:.8rem">Max 200 MB · CSV format only</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Prediction logic ──────────────────────────────────────────────────────
    try:
        uploaded_df = pd.read_csv(uploaded_file)

        if "customerID" in uploaded_df.columns:
            uploaded_df = uploaded_df.drop(columns=["customerID"])
        if "Churn" in uploaded_df.columns:
            uploaded_df = uploaded_df.drop(columns=["Churn"])

        model = joblib.load("models/churn_model.pkl")

        probabilities = model.predict_proba(uploaded_df)[:, 1]
        uploaded_df["Churn Probability"] = probabilities
        uploaded_df["Risk Bucket"] = uploaded_df["Churn Probability"].apply(
            lambda x:
            "Critical" if x >= 0.80
            else "High" if x >= 0.60
            else "Medium" if x >= 0.40
            else "Low"
        )

        # Summary strip
        counts = uploaded_df["Risk Bucket"].value_counts()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🔴 Critical", counts.get("Critical", 0))
        c2.metric("🟠 High",     counts.get("High", 0))
        c3.metric("🟡 Medium",   counts.get("Medium", 0))
        c4.metric("🟢 Low",      counts.get("Low", 0))

        st.markdown('<p class="section-label" style="margin-top:1.5rem">Prediction Results</p>', unsafe_allow_html=True)
        st.dataframe(uploaded_df, use_container_width=True, hide_index=True)

        st.download_button(
            label="↓  Download Predictions",
            data=uploaded_df.to_csv(index=False),
            file_name="churn_predictions.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Prediction failed — {str(e)}")
