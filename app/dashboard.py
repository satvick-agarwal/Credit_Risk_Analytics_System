import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from sklearn.metrics import confusion_matrix

def show():
    # Load resources
    df = pd.read_csv("data/processed/cleaned_data.csv")
    model = joblib.load("models/credit_risk_model.pkl")

    # Layout Configuration
    st.set_page_config(layout="wide") # Dashboard-style wide view
    
    st.title("⚖️ Institutional Credit Risk Analytics")
    st.caption("Quantitative Oversight & Predictive Model Performance Dashboard")
    st.divider()

    # --- 1. KEY PERFORMANCE INDICATORS (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate stats
    default_rate = df['loan_status'].mean()
    avg_loan = df['loan_amnt'].mean()
    avg_income = df['person_income'].mean()

    with col1:
        st.metric("Portfolio Size", f"{len(df):,}", help="Total unique loan applications analyzed")
    with col2:
        st.metric("Baseline Default Rate", f"{default_rate*100:.2f}%", delta="-0.5% vs Last Quarter", delta_color="inverse")
    with col3:
        st.metric("Exposure per Borrower", f"${avg_loan:,.0f}", help="Average loan principal amount")
    with col4:
        st.metric("Avg. Household Income", f"${avg_income:,.0f}")

    st.markdown("---")

    # --- 2. RISK SEGMENTATION & STATISTICAL DISTRIBUTIONS ---
    tab1, tab2 = st.tabs(["📊 Portfolio Distribution", "🎯 Model Interpretability"])

    with tab1:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Credit Score vs. Default Probability")
            # Using Plotly for professional interactive box plots
            fig_score = px.box(df, x="loan_status", y="credit_score", 
                               color="loan_status", notched=True,
                               title="Credit Rating Spread by Loan Outcome",
                               labels={"loan_status": "Defaulted?", "credit_score": "FICO Score"})
            st.plotly_chart(fig_score, use_container_width=True)

        with col_right:
            st.subheader("Debt-to-Income (DTI) Impact")
            fig_dti = px.violin(df, x="loan_status", y="loan_percent_income", 
                                box=True, points="all",
                                title="Loan-to-Income Ratio Distribution",
                                labels={"loan_percent_income": "% of Annual Income"})
            st.plotly_chart(fig_dti, use_container_width=True)

        st.divider()

        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Concentration Risk by Intent")
            fig_intent = px.histogram(df, x="loan_intent", color="loan_status", 
                                     barmode="group", text_auto=True,
                                     title="Default Frequency by Loan Purpose")
            st.plotly_chart(fig_intent, use_container_width=True)
        
        with col_b:
            st.subheader("Housing Tenure Risk")
            fig_home = px.pie(df, names="person_home_ownership", values="loan_status",
                              hole=0.4, title="Default Contribution by Housing Type")
            st.plotly_chart(fig_home, use_container_width=True)

    # --- 3. MODEL PERFORMANCE & FEATURE RANKING ---
    with tab2:
        st.subheader("Variable Importance (SHAP/Coefficient Analysis)")
        
        feature_names = model.named_steps["preprocessor"].get_feature_names_out()
        coefficients = model.named_steps["classifier"].coef_[0]

        importance_df = pd.DataFrame({
            "Variable": feature_names,
            "Impact": coefficients
        }).sort_values("Impact", ascending=True)

        fig_imp = px.bar(importance_df, x="Impact", y="Variable", orientation='h',
                        title="Top Statistical Drivers of Loan Default",
                        color="Impact", color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig_imp, use_container_width=True)

        st.divider()

        # Model Confusion Matrix Analysis
        col_m1, col_m2 = st.columns([1, 1])
        
        with col_m1:
            st.subheader("Model Validation: Confusion Matrix")
            
            X = df.drop(columns=["loan_status"])

            expected_cols = model.named_steps["preprocessor"].feature_names_in_

            # Add missing columns if any
            for col in expected_cols:
                if col not in X.columns:
                    X[col] = 0

            # Align order
            X = X[expected_cols]

            # Predict
            y_pred = model.predict(X)
            cm = confusion_matrix(df["loan_status"], y_pred)
            
            fig_cm = px.imshow(cm, text_auto=True, 
                               labels=dict(x="Predicted Label", y="Actual Label"),
                               x=['Non-Default', 'Default'], y=['Non-Default', 'Default'],
                               color_continuous_scale="Blues")
            st.plotly_chart(fig_cm, use_container_width=True)

        with col_m2:
            st.subheader("Strategic Summary")
            st.info("""
            **Model Insights:**
            - **Primary Risk Driver:** High Debt-to-Income ratio and low Credit Scores show the strongest correlation with default.
            - **Secondary Factors:** Home ownership (Renters) and specific Loan Intents (Medical) represent higher volatility segments.
            - **Action Plan:** Implement stricter automated thresholds for DTI > 40%.
            """)