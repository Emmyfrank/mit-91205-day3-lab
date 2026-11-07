# lab2_managed_vs_external.py - Simulate managed vs external tables
import os
import shutil
import json
import pandas as pd

# ---- Set up two tables in two directories ----
os.makedirs("warehouse/managed_table", exist_ok=True)
os.makedirs("external_data", exist_ok=True)

df = pd.read_csv("sales.csv").head(1000)
df.to_csv("warehouse/managed_table/data.csv", index=False)
df.to_csv("external_data/raw_data.csv", index=False)

# Simulate the metastore: a small JSON file that names the table and its directory
with open("metastore.json", "w") as f:
    json.dump({
        "tables": {
            "managed_table": {
                "type": "MANAGED",
                "location": "warehouse/managed_table",
                "owner": "hive",
            },
            "external_table": {
                "type": "EXTERNAL",
                "location": "external_data",
                "owner": "other_team",
            }
        }
    }, f, indent=2)

print("Before any DROP:")
print(f"  Managed data exists:  {os.path.exists('warehouse/managed_table/data.csv')}")
print(f"  External data exists: {os.path.exists('external_data/raw_data.csv')}")
print()

# ---- DROP managed table ----
print(">>> DROP TABLE managed_table <<<")
meta = json.load(open("metastore.json"))
if meta["tables"]["managed_table"]["type"] == "MANAGED":
    # Hive deletes the directory and its files
    shutil.rmtree(meta["tables"]["managed_table"]["location"])
    del meta["tables"]["managed_table"]
json.dump(meta, open("metastore.json", "w"), indent=2)

print(f"  Managed data exists after DROP: {os.path.exists('warehouse/managed_table/data.csv')}")
print()

# ---- DROP external table ----
print(">>> DROP TABLE external_table <<<")
meta = json.load(open("metastore.json"))
if meta["tables"]["external_table"]["type"] == "EXTERNAL":
    # Hive deletes only the metadata, NOT the files
    location = meta["tables"]["external_table"]["location"]
    del meta["tables"]["external_table"]
    # Do not touch the location!
json.dump(meta, open("metastore.json", "w"), indent=2)

print(f"  External data exists after DROP: {os.path.exists('external_data/raw_data.csv')}")
print(f"  Rows still readable: {len(pd.read_csv('external_data/raw_data.csv'))}")