# MIT 91205 — Big Data Analytics: Day 3 Practical

This repository contains the practical assignments and lab implementations for Day 3 of the Big Data Analytics course, focusing on Hive, Pig, and schema-on-read concepts.

## 🛠️ Tech Stack & Environment
* **Language:** Python
* **Environment:** macOS (Intel 2019 MacBook Pro), Zsh, Python Virtual Environment (`day3env`)
* **Libraries:** DuckDB, Pandas, Pyarrow, Matplotlib

## 📂 Lab Structure
* `generate_datasets.py`: Generates the standardized course datasets (`sales.csv`, `products.csv`, partitions, and hash buckets).
* `lab1_schema_on_read.py`: Schema-on-Read inference and SerDe (CSV vs. JSON) comparisons.
* `lab2_managed_vs_external.py`: Simulation of managed vs. external tables and storage lifecycle behavior upon `DROP TABLE`.
* `lab3_partitioning.py`: Directory-based partitioning and partition pruning performance tests.
* `lab4a_formats.py` & `lab4b_bucketing.py`: Storage format benchmarks (CSV, JSON, Parquet) and hash-based bucketing optimization.
* `lab5_hiveql.py`: HiveQL-style analytics queries and views using DuckDB.
* `lab6_pig_latin.py`: Simulating Pig Latin dataflow pipelines using Pandas.
* `lab7_udf.py`: Custom User-Defined Functions (UDFs) for row-level transformations.

## 🚀 How to Run
1. Clone the repository and navigate into the folder.
2. Create and activate your virtual environment:
   ```bash
   python3 -m venv day3env
   source day3env/bin/activate