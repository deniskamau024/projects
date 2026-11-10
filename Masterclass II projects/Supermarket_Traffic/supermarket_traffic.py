import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. Set seed for reproducible results
np.random.seed(42)

# 2. Generate 18 months of daily dates (May 2025 – October 2026)
dates = pd.date_range(start="2025-05-01", end="2026-10-31", freq="D")
n_days = len(dates)

# 3. Build realistic daily transaction counts using NumPy
# Base foot traffic + slight organic growth over 18 months
base_traffic = 1200 + np.linspace(0, 180, n_days)

# Seasonal multipliers by month (Higher in December, lower in February)
month_multipliers = {
    1: 0.95,   # January (post-holiday cooldown)
    2: 0.82,   # February (lowest seasonal dip)
    3: 0.96,   # March
    4: 1.02,   # April (Easter shopping)
    5: 0.98,   # May
    6: 1.00,   # June
    7: 1.03,   # July
    8: 1.05,   # August (school holidays)
    9: 0.99,   # September
    10: 1.01,  # October
    11: 1.12,  # November (early festive buildup)
    12: 1.38,  # December (peak festive surge)
}
seasonal_factor = np.array([month_multipliers[d.month] for d in dates])

# Weekend boost (Fridays, Saturdays, Sundays see higher foot traffic)
weekend_boost = np.where(dates.dayofweek >= 4, 1.15, 0.94)

# Random daily fluctuation
daily_noise = np.random.normal(loc=1.0, scale=0.06, size=n_days)

# Combine components into integer daily transaction counts
daily_transactions = np.round(
    base_traffic * seasonal_factor * weekend_boost * daily_noise
).astype(int)

df = pd.DataFrame({"transactions": daily_transactions}, index=dates)

# 4. Resample to monthly totals and calculate 30-day rolling average
# Multiplying the 30-day daily average by 30 puts it on the exact same monthly scale as the bars
monthly_totals = df["transactions"].resample("ME").sum()
rolling_30d_monthly_pace = df["transactions"].rolling(window=30, min_periods=1).mean() * 30

# 5. Plot monthly bars alongside the 30-day rolling trend
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(12, 6.5))

# Bar chart for monthly totals (centered nicely on each month)
bar_dates = monthly_totals.index - pd.Timedelta(days=14)
ax.bar(
    bar_dates,
    monthly_totals.values,
    width=20,
    color="#4A90D9",
    alpha=0.75,
    label="Monthly Total Transactions",
)

# Line chart for 30-day rolling average
ax.plot(
    rolling_30d_monthly_pace.index,
    rolling_30d_monthly_pace.values,
    color="#D9534F",
    linewidth=2.5,
    label="30-Day Rolling Trend (30-Day Pace)",
)

# 6. Clear title, labels, and annotations for a non-technical manager
ax.set_title(
    "Nairobi Supermarket Chain: 18-Month Foot Traffic & Seasonal Trend",
    fontsize=15,
    fontweight="bold",
    pad=15,
)
ax.set_xlabel("Month", fontsize=12, labelpad=10)
ax.set_ylabel("Number of Customer Transactions", fontsize=12, labelpad=10)

# Format y-axis with commas and x-axis with Month + Year
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

# Annotate December peak and February dip for quick executive reading
dec_date = pd.Timestamp("2025-12-15")
dec_val = monthly_totals.loc["2025-12-31"]
ax.annotate(
    f"Dec Peak\n({dec_val:,})",
    xy=(dec_date, dec_val),
    xytext=(dec_date - pd.Timedelta(days=45), dec_val + 3500),
    arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=1.2),
    fontsize=10,
    fontweight="bold",
    color="#2C3E50",
)

feb_date = pd.Timestamp("2026-02-14")
feb_val = monthly_totals.loc["2026-02-28"]
ax.annotate(
    f"Feb Low\n({feb_val:,})",
    xy=(feb_date, feb_val),
    xytext=(feb_date + pd.Timedelta(days=20), feb_val - 6000),
    arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=1.2),
    fontsize=10,
    fontweight="bold",
    color="#2C3E50",
)

ax.set_ylim(0, monthly_totals.max() * 1.18)
ax.legend(loc="upper left", frameon=True, fontsize=11)
plt.tight_layout()

# 7. Save chart as PNG
output_file = "supermarket_foot_traffic_trend.png"
plt.savefig(output_file, dpi=300)
print(f"Chart successfully saved as '{output_file}'")