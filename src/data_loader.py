from sqlalchemy import create_engine
import pandas as pd

# change username/password if needed
engine = create_engine("postgresql://postgres:ADMIN69@localhost:5432/credit_risk_db")

df = pd.read_csv("data/processed/cleaned_data.csv")

df.to_sql("loan_data", engine, if_exists="append", index=False)

print("✅ Data loaded successfully")