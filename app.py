import streamlit as st

from dashboard.home import show_home
from dashboard.customer_dashboard import show_customer_dashboard
from dashboard.churn_dashboard import show_churn_dashboard
from dashboard.revenue_dashboard import show_revenue_dashboard
from dashboard.prediction_dashboard import show_prediction_dashboard
from dashboard.recommendation_dashboard import show_recommendation_dashboard

st.set_page_config(
    page_title="Customer Churn Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Customer Analytics",
        "Churn Analytics",
        "Revenue Analytics",
        "Prediction Module",
        "Retention Recommendations"
    ]
)

if page == "Home":
    show_home()

elif page == "Customer Analytics":
    show_customer_dashboard()

elif page == "Churn Analytics":
    show_churn_dashboard()

elif page == "Revenue Analytics":
    show_revenue_dashboard()

elif page == "Prediction Module":
    show_prediction_dashboard()

elif page == "Retention Recommendations":
    show_recommendation_dashboard()