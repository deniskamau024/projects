# Mombasa Microfinance Loan Repayment Analysis

## Board Briefing: Loan Size & Repayment Timing
There is a strong positive link between loan size and repayment timing, meaning borrowers with larger loans generally take more days to make their first payment.

## Overview
This project analyzes 150 fictional loan records (Mombasa_loans.csv) for a Mombasa-based microfinance institution to help board members understand typical borrowing behavior, flag unusually large or small loans, and evaluate how loan size affects initial repayment speed.

## Key Findings
* *Typical Loan Size:* Most loans cluster around a median of *KES 46,350* (mean: *KES 47,298, standard deviation: **KES 20,256), with the middle 50% of loans falling between **KES 39,350* (25th percentile) and *KES 53,425* (75th percentile).
* *Outlier Loans (IQR Method):* Six loans fall outside the standard range (KES 18,238 to KES 74,538):
  * *Unusually Small Loans:* MFI-1012 (KES 4,500) and MFI-1089 (KES 5,200)
  * *Unusually Large Loans:* MFI-1005 (KES 165,000), MFI-1044 (KES 142,000), MFI-1118 (KES 185,000), and MFI-1142 (KES 128,000)

## Loan Distribution Histogram
![Distribution of Loan Amounts](loan_histogram.png)

## Project Files
* Mombasa_loans.csv — Dataset containing 150 loan records (loan_id, amount_kes, days_to_first_repayment, county).
* Loans_analysis.py — Python script that runs the statistical summary, detects IQR outliers, calculates correlation, and generates the histogram.
* loan_histogram.png — Visual distribution of disbursed loan amounts.

## How to Run
1. Install the required Python libraries:
   bash
   pip install pandas numpy matplotlib
   
2. Run the analysis script:
   bash
   python Loans_analysis.py