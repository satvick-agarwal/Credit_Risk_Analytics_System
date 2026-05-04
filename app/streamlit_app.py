import streamlit as st

st.set_page_config(page_title="Credit Risk System", layout="wide")

st.title("🏦 Credit Risk Analytics System")

# Sidebar Navigation
tab1, tab2 = st.tabs(
    ["Dashboard", "Predictor"]
)

with tab1: 
    import dashboard
    dashboard.show()

with tab2:
    import predictor
    predictor.show()