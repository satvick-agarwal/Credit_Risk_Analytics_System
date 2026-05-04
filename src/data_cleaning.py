import pandas as pd
df=pd.read_csv("data/raw/loan_data.csv")

#cleaning the invalid rows

#removing rows with invalid age (<18 or >75)
df = df[(df["person_age"] >= 18) & (df["person_age"] <= 75)]

#removing row with invalid loan_percent_income (<=0 or >1)
df["loan_percent_income"] = df["loan_amnt"] / df["person_income"]
# print(df[df["loan_percent_income"] <= 0].shape[0])  output: 0
# print(df[df["loan_percent_income"] > 1].shape[0]) output: 0

df.to_csv("data/processed/cleaned_data.csv", index=False)
print("✅ Cleaned data saved successfully")