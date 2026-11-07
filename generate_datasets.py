# generate_datasets.py
# MIT 91205 - Day 3 Practical
# Generates sales.csv, products.csv, stores.csv, sales.json,
# and the partitioned + bucketed directories used in Labs 3-4.

import os
import shutil
import glob
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime

np.random.seed(42)

# ============================================================
# 1. Products: 20 items in 4 categories
# ============================================================
categories = ["Electronics", "Furniture", "Office", "Garden"]
products = pd.DataFrame({
    "product_id": list(range(1, 21)),
    "name":       [f"Product-{i}" for i in range(1, 21)],
    "category":   np.random.choice(categories, 20),
    "unit_price": np.round(np.random.uniform(10, 1500, 20), 2),
})
products.to_csv("products.csv", index=False)
print(f"products.csv: {len(products)} rows")

# ============================================================
# 2. Stores: 8 stores across 4 regions
# ============================================================
regions_cycle = ["North", "South", "East", "West"] * 2
stores = pd.DataFrame({
    "store_id": list(range(1, 9)),
    "name":     [f"Store-{i}" for i in range(1, 9)],
    "region":   regions_cycle,
})
stores.to_csv("stores.csv", index=False)
print(f"stores.csv: {len(stores)} rows")

# ============================================================
# 3. Sales: 20,000 transactions over 6 months
# ============================================================
n_sales = 20000
product_ids = np.random.choice(products["product_id"], n_sales)
store_ids   = np.random.choice(stores["store_id"], n_sales)
quantities  = np.random.randint(1, 10, n_sales)

price_map = dict(zip(products["product_id"], products["unit_price"]))
amounts   = [round(q * price_map[pid], 2)
             for q, pid in zip(quantities, product_ids)]

months = np.random.randint(1, 7, n_sales)
days   = np.random.randint(1, 29, n_sales)
dates  = [datetime(2024, m, d).strftime("%Y-%m-%d")
          for m, d in zip(months, days)]

sales = pd.DataFrame({
    "sale_id":    list(range(1, n_sales + 1)),
    "product_id": product_ids,
    "store_id":   store_ids,
    "quantity":   quantities,
    "amount":     amounts,
    "dt":         dates,
})
sales.to_csv("sales.csv", index=False)
print(f"sales.csv: {len(sales)} rows")

# ============================================================
# 4. sales.json: same data in JSON (demonstrates SerDe)
# ============================================================
sales.head(500).to_json("sales.json", orient="records")
print(f"sales.json: {min(500, len(sales))} rows (first 500 for SerDe demo)")

# ============================================================
# 5. Partitioned directory: one file per month (Lab 3)
# ============================================================
if os.path.exists("sales_partitioned"):
    shutil.rmtree("sales_partitioned")
for month in range(1, 7):
    dt_prefix = f"2024-{month:02d}"
    os.makedirs(f"sales_partitioned/dt={dt_prefix}", exist_ok=True)
    monthly = sales[sales["dt"].str.startswith(dt_prefix)]
    monthly.to_csv(f"sales_partitioned/dt={dt_prefix}/sales.csv", index=False)
print(f"sales_partitioned/: 6 monthly partitions")

# ============================================================
# 6. Bucketed directory: 4 hash-based buckets (Lab 4)
# ============================================================
if os.path.exists("sales_bucketed"):
    shutil.rmtree("sales_bucketed")
os.makedirs("sales_bucketed")
NUM_BUCKETS = 4
for pid, group in sales.groupby("product_id"):
    bucket = int(hashlib.md5(str(pid).encode()).hexdigest(), 16) % NUM_BUCKETS
    group.to_csv(f"sales_bucketed/bucket_{bucket}.csv",
                 mode="a",
                 header=not os.path.exists(f"sales_bucketed/bucket_{bucket}.csv"),
                 index=False)
print(f"sales_bucketed/: {NUM_BUCKETS} hash buckets")

print("\nAll datasets generated.")