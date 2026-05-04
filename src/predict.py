import joblib
import pandas as pd

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load("models/credit_risk_model.pkl")


# -----------------------------
# Risk categorization
# -----------------------------
def risk_category(prob):
    if prob < 0.3:
        return "Low Risk"
    elif prob < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"

def generate_explanation(df, prob):

    reasons = []

    # Strong signals
    if df["has_previous_default"].iloc[0] == 1:
        reasons.append("Previous loan default history")

    if df["loan_percent_income"].iloc[0] > 0.3:
        reasons.append("Loan amount is high relative to income")

    if df["credit_score"].iloc[0] < 600:
        reasons.append("Low credit score")

    if df["loan_int_rate"].iloc[0] > 15:
        reasons.append("High interest rate (risk indicator)")

    if df["person_emp_exp"].iloc[0] < 2:
        reasons.append("Low employment experience")

    # 🔥 Improved fallback
    if not reasons:
        if prob < 0.1:
            reasons.append("Very strong financial and credit profile")
        elif prob < 0.3:
            reasons.append("Moderately stable financial profile")
        elif prob < 0.6:
            reasons.append("Moderate financial risk due to loan burden")
        else:
            reasons.append("Elevated risk based on combined financial indicators")

    return reasons

def decision_category(prob, has_previous_default):

    if has_previous_default == 1:
        return "Reject"

    if prob >= 0.80:
        return "Reject"
    elif prob >= 0.50:
        return "Manual Review"
    else:
        return "Approve"
    
# -----------------------------
# Prediction function
# -----------------------------
def predict_risk(input_data: dict):

    df = pd.DataFrame([input_data])

    df["loan_percent_income"] = df["loan_amnt"] / df["person_income"]

    df["has_previous_default"] = df["previous_loan_defaults_on_file"].map({
        "Yes": 1,
        "No": 0
    })

    prob = model.predict_proba(df)[0][1]

    reasons = generate_explanation(df, prob)

    # Override rule
    if df["has_previous_default"].iloc[0] == 1:
        return {
            "probability": round(float(prob), 4),
            "risk": "High Risk (Previous Default)",
            "decision": "Reject",
            "reasons": reasons
        }
    decision = decision_category(prob, df["has_previous_default"].iloc[0])

    return {
        "probability": round(float(prob), 4),
        "risk": risk_category(prob),
        "decision": decision,
        "reasons": reasons
    }

