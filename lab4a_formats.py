# lab4a_formats.py - Compare CSV, JSON, Parquet
import os
import time
import pandas as pd

df = pd.read_csv("sales.csv")

# Write the same data in three formats
df.to_csv("sales_format.csv", index=False)
df.to_json("sales_format.json", orient="records")
df.to_parquet("sales_format.parquet", index=False)

# Compare file sizes
print("File sizes:")
formats = [("csv", "sales_format.csv"),
           ("json", "sales_format.json"),
           ("parquet", "sales_format.parquet")]

for name, path in formats:
    size = os.path.getsize(path)
    print(f"  {name:8s} {size:>10,} bytes")
print()

# Time a single-column query from each
print("Querying only 'product_id' (single column):")
for name, path in formats:
    start = time.time()
    if name == "csv":
        d = pd.read_csv(path, usecols=["product_id"])
    elif name == "json":
        d = pd.read_json(path, orient="records")
        d = d[["product_id"]]
    else:
        d = pd.read_parquet(path, columns=["product_id"])
    elapsed = time.time() - start
    print(f"  {name:8s} {elapsed:.4f}s   ({len(d):,} rows read)")
print()

# Time a full-table query from each
print("Querying ALL columns:")
for name, path in formats:
    start = time.time()
    if name == "csv":
        d = pd.read_csv(path)
    elif name == "json":
        d = pd.read_json(path, orient="records")
    else:
        d = pd.read_parquet(path)
    elapsed = time.time() - start
    print(f"  {name:8s} {elapsed:.4f}s   ({len(d):,} rows read)")