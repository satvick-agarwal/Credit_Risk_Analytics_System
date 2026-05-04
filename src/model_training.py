import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)


# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/processed/cleaned_data.csv")


# -----------------------------
# Feature Engineering
# -----------------------------
df["loan_percent_income"] = df["loan_amnt"] / df["person_income"]

df["has_previous_default"] = df["previous_loan_defaults_on_file"].map({
    "Yes": 1,
    "No": 0
})

# -----------------------------
# Select Features
# -----------------------------
features = [
    "has_previous_default",
    "loan_percent_income",
    "credit_score",
    "loan_intent",
    "person_home_ownership",
    "loan_int_rate",
    "person_income",
    "loan_amnt",
    "person_emp_exp",
    "cb_person_cred_hist_length",
    "person_age",
    "person_education"
]

target = "loan_status"

X = df[features]
y = df[target]


# -----------------------------
# Numeric + Categorical Columns
# -----------------------------
numeric_features = [
    "has_previous_default",
    "loan_percent_income",
    "credit_score",
    "loan_int_rate",
    "person_income",
    "loan_amnt",
    "person_emp_exp",
    "cb_person_cred_hist_length",
    "person_age"
]

categorical_features = [
    "loan_intent",
    "person_home_ownership",
    "person_education"
]


# -----------------------------
# Preprocessing
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)


# -----------------------------
# Model Pipeline
# -----------------------------
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)


# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------
# Train Model
# -----------------------------
model.fit(X_train, y_train)


# -----------------------------
# Predictions
# -----------------------------

y_prob = model.predict_proba(X_test)[:, 1]
threshold = 0.46
y_pred = (y_prob >= threshold).astype(int)


# -----------------------------
# Evaluation
# -----------------------------
print("Model Evaluation")
print("-----------------")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "models/credit_risk_model.pkl")

print("\n✅ Model trained and saved successfully.")
