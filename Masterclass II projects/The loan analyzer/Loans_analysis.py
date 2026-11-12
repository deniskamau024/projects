import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load csv directly into pandas dataframe
df = pd.read_csv("Mombasa_loans.csv")

# Run full ststistical summary using describe
print("=====FULL STATISTICAL SUMMARY=====")
print(df.describe())


# Identifying Outliers using the IQR method

Q1 = df["amount_kes"].quantile(0.25)
Q3 = df["amount_kes"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df["amount_kes"] < lower) | (df["amount_kes"] > upper)]
print("\n=== OUTLIER LOAN IDs (IQR METHOD) ===")
print("Outlier IDs:", outliers["loan_id"].tolist())
print()
print(outliers)

# 4. Calculate correlation and state what it means in one plain sentence
corr = df["amount_kes"].corr(df["days_to_first_repayment"])

print("\n=== CORRELATION ===")
print(f"Correlation: {corr:.2f}")
print("There is a strong positive link between loan size and repayment timing, meaning borrowers with larger loans generally take more days to make their first payment.")

# 5. Plot a histogram of loan amounts
plt.figure(figsize=(9, 5))
plt.hist(df["amount_kes"], bins=15, color="steelblue", edgecolor="black")
plt.title("Distribution of Loan Amounts (Mombasa Microfinance)")
plt.xlabel("Loan Amount (KES)")
plt.ylabel("Number of Loans")
plt.tight_layout()
plt.savefig("loan_histogram.png")
plt.show()