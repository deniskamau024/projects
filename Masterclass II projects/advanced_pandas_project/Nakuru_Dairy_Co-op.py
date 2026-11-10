import pandas as pd

# 1. Create realistic sample data for 12 farmers across 3 Nakuru zones
farmer_details_data = [
    {"farmer_name": "James Kamau", "zone": "Bahati", "payment_rate_per_litre": 50},
    {"farmer_name": "Mary Wanjiku", "zone": "Bahati", "payment_rate_per_litre": 52},
    {"farmer_name": "Peter Njoroge", "zone": "Bahati", "payment_rate_per_litre": 50},
    {"farmer_name": "Grace Muthoni", "zone": "Bahati", "payment_rate_per_litre": 51},
    {"farmer_name": "Samuel Kiprop", "zone": "Njoro", "payment_rate_per_litre": 48},
    {"farmer_name": "Esther Chebet", "zone": "Njoro", "payment_rate_per_litre": 50},
    {"farmer_name": "David Ochieng", "zone": "Njoro", "payment_rate_per_litre": 49},
    {"farmer_name": "Faith Nyambura", "zone": "Njoro", "payment_rate_per_litre": 50},
    {"farmer_name": "John Koech", "zone": "Rongai", "payment_rate_per_litre": 47},
    {"farmer_name": "Alice Cherono", "zone": "Rongai", "payment_rate_per_litre": 48},
    {"farmer_name": "Joseph Mwangi", "zone": "Rongai", "payment_rate_per_litre": 47},
    {"farmer_name": "Sarah Jepchirchir", "zone": "Rongai", "payment_rate_per_litre": 49},
]

# Daily milk collection records for the current month
milk_collection_data = [
    # Bahati Zone
    {"farmer_name": "James Kamau", "date": "2026-11-01", "litres": 45},
    {"farmer_name": "James Kamau", "date": "2026-11-02", "litres": 48},
    {"farmer_name": "Mary Wanjiku", "date": "2026-11-01", "litres": 62},
    {"farmer_name": "Mary Wanjiku", "date": "2026-11-02", "litres": 65},
    {"farmer_name": "Peter Njoroge", "date": "2026-11-01", "litres": 38},
    {"farmer_name": "Peter Njoroge", "date": "2026-11-02", "litres": 40},
    {"farmer_name": "Grace Muthoni", "date": "2026-11-01", "litres": 51},
    {"farmer_name": "Grace Muthoni", "date": "2026-11-02", "litres": 49},
    # Njoro Zone
    {"farmer_name": "Samuel Kiprop", "date": "2026-11-01", "litres": 55},
    {"farmer_name": "Samuel Kiprop", "date": "2026-11-02", "litres": 58},
    {"farmer_name": "Esther Chebet", "date": "2026-11-01", "litres": 70},
    {"farmer_name": "Esther Chebet", "date": "2026-11-02", "litres": 68},
    {"farmer_name": "David Ochieng", "date": "2026-11-01", "litres": 42},
    {"farmer_name": "David Ochieng", "date": "2026-11-02", "litres": 44},
    {"farmer_name": "Faith Nyambura", "date": "2026-11-01", "litres": 50},
    {"farmer_name": "Faith Nyambura", "date": "2026-11-02", "litres": 52},
    # Rongai Zone
    {"farmer_name": "John Koech", "date": "2026-11-01", "litres": 40},
    {"farmer_name": "John Koech", "date": "2026-11-02", "litres": 43},
    {"farmer_name": "Alice Cherono", "date": "2026-11-01", "litres": 58},
    {"farmer_name": "Alice Cherono", "date": "2026-11-02", "litres": 60},
    {"farmer_name": "Joseph Mwangi", "date": "2026-11-01", "litres": 35},
    {"farmer_name": "Joseph Mwangi", "date": "2026-11-02", "litres": 37},
    {"farmer_name": "Sarah Jepchirchir", "date": "2026-11-01", "litres": 64},
    {"farmer_name": "Sarah Jepchirchir", "date": "2026-11-02", "litres": 66},
]

df_farmers = pd.DataFrame(farmer_details_data)
df_collections = pd.DataFrame(milk_collection_data)

# Optional: Save sample spreadsheets to CSV so the script mirrors real file inputs
df_farmers.to_csv("farmer_details.csv", index=False)
df_collections.to_csv("milk_collection.csv", index=False)

# 2. Load spreadsheets and filter for the target month
farmers = pd.read_csv("farmer_details.csv")
collections = pd.read_csv("milk_collection.csv")
collections["date"] = pd.to_datetime(collections["date"])

# Filter to the latest month present in the dataset
current_month = collections["date"].dt.to_period("M").max()
monthly_collections = collections[collections["date"].dt.to_period("M") == current_month]

# 3. Merge DataFrames on farmer_name and calculate payout per delivery
merged_df = pd.merge(monthly_collections, farmers, on="farmer_name", how="left")
merged_df["payout"] = merged_df["litres"] * merged_df["payment_rate_per_litre"]

# 4. Pivot the result by zone for total litres and total payout
zone_pivot = merged_df.pivot_table(
    index="zone",
    values=["litres", "payout"],
    aggfunc="sum"
)

# 5. Identify the top farmer per zone by total litres delivered
farmer_totals = (
    merged_df.groupby(["zone", "farmer_name"], as_index=False)["litres"]
    .sum()
)
top_farmers = (
    farmer_totals.sort_values("litres", ascending=False)
    .drop_duplicates("zone")
    .set_index("zone")["farmer_name"]
)

# 6. Combine into a clean summary table with the three requested columns
summary = pd.DataFrame({
    "Total Litres This Month": zone_pivot["litres"].map("{:,.0f} L".format),
    "Total Payout": zone_pivot["payout"].map("KES {:,.2f}".format),
    "Top Farmer": top_farmers
})
summary.index.name = "Zone"

# 7. Print clean, screenshot-ready output
border = "=" * 68
print(f"\n{border}")
print(f"   NAKURU DAIRY CO-OP — MONTHLY ZONE SUMMARY ({current_month})")
print(border)
print(summary.to_string())
print(f"{border}\n")

