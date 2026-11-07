# lab4b_bucketing.py - Bucketing simulation
import os
import hashlib
import glob
import time
import pandas as pd

df = pd.read_csv("sales.csv")
NUM_BUCKETS = 4

print("Bucket layout on disk:")
files = sorted(glob.glob("sales_bucketed/bucket_*.csv"))
for f in files:
    n = len(pd.read_csv(f))
    print(f"  {f}: {n:,} rows, {os.path.getsize(f):,} bytes")
print()

# Which bucket holds product_id=5?
target = 5
bucket = int(hashlib.md5(str(target).encode()).hexdigest(), 16) % NUM_BUCKETS
print(f"Product {target} → bucket {bucket} (from hash)")
print()

# Query WITHOUT bucketing: read everything
print("Query product_id=5 WITHOUT bucketing:")
start = time.time()
all_data = pd.concat([pd.read_csv(f) for f in files])
result = all_data[all_data["product_id"] == target]
print(f"  Rows read: {len(all_data):,}")
print(f"  Time: {time.time() - start:.4f}s")
print(f"  Matching rows: {len(result)}")
print()

# Query WITH bucketing: read only the target bucket
print(f"Query product_id=5 WITH bucketing (only bucket {bucket}):")
start = time.time()
bucket_data = pd.read_csv(f"sales_bucketed/bucket_{bucket}.csv")
result2 = bucket_data[bucket_data["product_id"] == target]
print(f"  Rows read: {len(bucket_data):,}")
print(f"  Time: {time.time() - start:.4f}s")
print(f"  Matching rows: {len(result2)}")