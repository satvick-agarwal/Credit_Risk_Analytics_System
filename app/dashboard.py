import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def show():
    st.header("📊 Credit Risk Dashboard")

    df = pd.read_csv("data/processed/cleaned_data.csv")

    # -----------------------------
    # Default Distribution
    # -----------------------------
    st.subheader("Default Distribution")

    fig, ax = plt.subplots()
    sns.countplot(x="loan_status", data=df, ax=ax)
    st.pyplot(fig)

    # -----------------------------
    # Credit Score vs Default
    # -----------------------------
    st.subheader("Credit Score vs Default")

    fig, ax = plt.subplots()
    sns.boxplot(x="loan_status", y="credit_score", data=df, ax=ax)
    st.pyplot(fig)

    # -----------------------------
    # Loan Burden
    # -----------------------------
    st.subheader("Loan Burden vs Default")

    fig, ax = plt.subplots()
    df["loan_percent_income"] = df["loan_amnt"] / df["person_income"]
    sns.boxplot(x="loan_status", y="loan_percent_income", data=df, ax=ax)
    st.pyplot(fig)

    st.markdown("### Key Insights")
    st.write("""
    - Lower credit score → higher default risk  
    - Higher loan burden → higher default probability  
    - Previous defaults strongly impact future risk  
    """)