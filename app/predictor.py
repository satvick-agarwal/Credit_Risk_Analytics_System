import streamlit as st
import pandas as pd
import joblib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.predict import predict_risk 

model = joblib.load("models/credit_risk_model.pkl")


def risk_category(prob):
    if prob < 0.3:
        return "🟢 Low Risk"
    elif prob < 0.6:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"


def show():
    # Page Header
    st.title("🏦 Credit Risk Assessment")
    st.markdown("""
        Enter the borrower's financial and personal details below to generate a 
        real-time risk profile and loan decision recommendation.
    """)
    st.divider()

    # Wrap inputs in a form for a professional submit-on-click experience
    with st.form("loan_application_form"):
        st.subheader("📝 Borrower Profile")
        
        # Column Layout for compact data entry
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", 18, 75, 25)
            education = st.selectbox("Education Level", ["High School", "Bachelor", "Master"])
            emp_exp = st.number_input("Work Experience (Years)", 0, 50, 3)

        with col2:
            income = st.number_input("Annual Income ($)", 1000, 1000000, 50000, step=1000)
            home = st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE"])
            prev_default = st.selectbox("Previous Default", ["No", "Yes"])

        with col3:
            credit_score = st.slider("Credit Score", 300, 850, 650)
            cred_hist = st.number_input("Credit History (Years)", 0, 30, 5)
            interest = st.number_input("Proposed Int. Rate (%)", 1.0, 40.0, 12.0)

        st.subheader("💰 Loan Details")
        col_a, col_b = st.columns(2)
        with col_a:
            loan_amnt = st.number_input("Requested Loan Amount ($)", 1000, 500000, 20000, step=500)
        with col_b:
            intent = st.selectbox("Loan Purpose", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE"])

        # Form Submission Button
        submit_button = st.form_submit_button("Generate Risk Assessment", use_container_width=True)

    # Logic execution triggers only on button click
    if submit_button:
        input_data = {
            "person_age": age,
            "person_income": income,
            "person_emp_exp": emp_exp,
            "person_home_ownership": home,
            "loan_amnt": loan_amnt,
            "loan_intent": intent,
            "loan_int_rate": interest,
            "credit_score": credit_score,
            "cb_person_cred_hist_length": cred_hist,
            "person_education": education,
            "previous_loan_defaults_on_file": prev_default
        }

        with st.spinner("Analyzing financial risk parameters..."):
            result = predict_risk(input_data)

        st.divider()
        
        # Professional Result Dashboard
        st.subheader("📊 Analysis Results")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Risk Level", result['risk'])
        res_col2.metric("Probability for De", f"{result['probability']:.2%}")
        res_col3.metric("Final Decision", result['decision'])

        # Visual Feedback
        if result["decision"] == "Reject":
            st.error(f"**Action Required:** High Risk detected. Loan should be rejected.")
        elif result["decision"] == "Review" or result["decision"] =="Manual Review":
            st.warning(f"**Action Required:** Medium Risk detected. Manual credit review recommended.")
        else:
            st.success(f"**Action Required:** Low Risk detected. Application meets approval criteria.")

        # Interpretability Section
        with st.expander("🔍 See Model Interpretation"):
            st.write("The following factors most heavily influenced this prediction:")
            for reason in result["reasons"]:
                st.markdown(f"- {reason}")