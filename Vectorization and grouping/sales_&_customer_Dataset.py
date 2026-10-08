import numpy as np
import pandas as pd

# Create a raw data set

np.random.seed(42)
n_rows = 10000

data = {
    "transaction_id":np.arange(10000, 10000 + n_rows),
    "region":np.random.choice(
        ["North","East","West","South"]
    ),
    "product_category":np.random.choice(
        ["electronics", "furniture", "clothing", "beauty"], size=n_rows
    ),
    "quantity":np.random.randint(1,10,size=n_rows),
    "unit_price":np.random.uniform(10.0,500.0,size=n_rows),
}

df = pd.DataFrame(data)

# Inject some intentional missing data values into the numeric columns
df.loc[df["quantity"] == 5, "quantity"] =np.nan

print ("---Initial Memory Profile---")
print(df.info())

# OPTIMIZATION TECHNIQUE: Downcasting and categoricals
# Convert objects with low crdinalities to 'category'
df["region"] = df["region"].astype("category")
df["product_category"] = df["product_category"].astype("category")

# Downcast numerical columns to save bytes
df["quantity"] =pd.to_numeric(df["quantity"],downcast="float")
df["unit_price"] = pd.to_numeric(df["unit_price"],downcast="float")

print("\n ---Optimized Memory Profile---")
print(df.info())

# Fix messy text strings globally across the column instantly
df["product_category"] = df["product_category"].str.strip().str.capitalize()

# Impute missing regions with a placeholder and quantities with the median
df["region"] = df["region"].fillna("Unknown")
df["quantity"] = df["quantity"].fillna(df["quantity"].median())

# VECTORIZATION: Calculate total revenue instantly without loops
df["total_revenue"] = df["quantity"] * df["unit_price"]

analytics_summary = (
    df.groupby(["region", "product_category"])
    .agg(
        total_sales_value=("total_revenue", "sum"),
        average_quantity_sold=("quantity", "mean"),
        transaction_count=("transaction_id", "count"),
    )
    .reset_index()
)

print("\n--- Final Analytics Insights (First 5 Rows) ---")
print(analytics_summary.head())
