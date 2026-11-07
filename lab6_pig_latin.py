# lab6_pig_latin.py - Simulating Pig Latin dataflows with Pandas
import pandas as pd

# Step 1: LOAD
sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")

# Step 2: FILTER (Transactions with amount > 1000)
high_val_sales = sales[sales["amount"] > 1000]

# Step 3: JOIN
joined_data = pd.merge(high_val_sales, products, on="product_id")

# Step 4: GROUP BY category
grouped = joined_data.groupby("category")

# Step 5: FOREACH ... GENERATE (Aggregating values per group)
pig_output = grouped.agg(
    high_val_count=("sale_id", "count"),
    total_high_val_revenue=("amount", "sum")
).reset_index()

print("--- Pig Latin Pipeline Output ---")
print(pig_output.to_string(index=False))