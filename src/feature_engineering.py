import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform feature engineering for credit risk analysis.
    Transforms raw borrower data into meaningful risk indicators.
    """

    # -------------------------------
    # 1. Recompute Loan-to-Income Ratio
    # -------------------------------
    df["loan_percent_income"] = df["loan_amnt"] / df["person_income"]

    # -------------------------------
    # 2. Income Segmentation
    # -------------------------------
    df["income_group"] = pd.qcut(
        df["person_income"],
        q=4,
        labels=["Low", "Medium", "High", "Very High"]
    )

    # -------------------------------
    # 3. Age Segmentation
    # -------------------------------
    df["age_group"] = pd.cut(
        df["person_age"],
        bins=[18, 25, 35, 45, 60, 75],
        labels=["18-25", "26-35", "36-45", "46-60", "60+"]
    )

    # -------------------------------
    # 4. Credit Score Bucketing
    # -------------------------------
    df["credit_score_category"] = pd.cut(
        df["credit_score"],
        bins=[300, 580, 670, 740, 800, 850],
        labels=["Poor", "Fair", "Good", "Very Good", "Excellent"]
    )

    # -------------------------------
    # 5. Previous Default Flag
    # -------------------------------
    df["has_previous_default"] = df["previous_loan_defaults_on_file"].map({
        "Yes": 1,
        "No": 0
    })

    # -------------------------------
    # 6. High Loan Burden Flag
    # -------------------------------
    df["high_loan_burden"] = (df["loan_percent_income"] > 0.4).astype(int)

    # -------------------------------
    # 7. Optional: Drop redundant column
    # -------------------------------
    # You can drop original categorical later if needed
    # df = df.drop(columns=["previous_loan_defaults_on_file"])

    return df


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical variables for ML models.
    """

    df_encoded = pd.get_dummies(df, drop_first=True)

    return df_encoded


# -------------------------------
# MAIN EXECUTION (for testing)
# -------------------------------
if __name__ == "__main__":

    # Load cleaned data
    df = pd.read_csv("data/processed/cleaned_data.csv")

    # Apply feature engineering
    df = create_features(df)

    # Encode features
    df_encoded = encode_features(df)

    # Save processed dataset
    df_encoded.to_csv("data/processed/final_features.csv", index=False)

    print("✅ Feature engineering completed and saved.")