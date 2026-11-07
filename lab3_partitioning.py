# lab3_partitioning.py - Partitioning and pruning
import glob
import time
import os
import pandas as pd

# ---- Show what partitions exist ----
files = sorted(glob.glob("sales_partitioned/dt=*/*.csv"))
print(f"Found {len(files)} partition files:")
for f in files:
    print(f"  {f}: {os.path.getsize(f):,} bytes")
print()

# ---- Query WITHOUT pruning: read all partitions ----
print("Query WITHOUT pruning (read all 6 months):")
start = time.time()
all_data = pd.concat([pd.read_csv(f) for f in files])
elapsed_all = time.time() - start
print(f"  Rows read: {len(all_data):,}")
print(f"  Time: {elapsed_all:.4f}s")
march_revenue_all = all_data[all_data["dt"].str.startswith("2024-03")]["amount"].sum()
print(f"  March revenue: ${march_revenue_all:,.2f}")
print()

# ---- Query WITH pruning: read only March ----
print("Query WITH pruning (read only dt=2024-03):")
start = time.time()
march_only = pd.read_csv("sales_partitioned/dt=2024-03/sales.csv")
elapsed_march = time.time() - start
print(f"  Rows read: {len(march_only):,}")
print(f"  Time: {elapsed_march:.4f}s")
march_revenue_pruned = march_only["amount"].sum()
print(f"  March revenue: ${march_revenue_pruned:,.2f}")
print()

# ---- Confirm identical results ----
print(f"Same result? {abs(march_revenue_all - march_revenue_pruned) < 0.01}")
print(f"Speedup: {elapsed_all / max(elapsed_march, 0.0001):.1f}x")
print(f"Rows avoided: {len(all_data) - len(march_only):,} "
      f"({100 * (1 - len(march_only) / len(all_data)):.0f}% pruned)")