# lab1_schema_on_read.py - Schema-on-read and SerDe demo
import duckdb

con = duckdb.connect()

# ---- Step 1: No declared schema, just ask DuckDB to infer it ----
print("Step 1: DuckDB infers the schema from the file")
schema = con.execute(
    "DESCRIBE SELECT * FROM read_csv_auto('sales.csv')").df()
print(schema[["column_name", "column_type"]].to_string(index=False))
print()

# ---- Step 2: Query the raw CSV directly ----
print("Step 2: Query the file directly, no CREATE TABLE needed")
result = con.execute("""
    SELECT dt, COUNT(*) AS n_sales, SUM(amount) AS revenue
    FROM read_csv_auto('sales.csv')
    GROUP BY dt
    ORDER BY dt
    LIMIT 5
""").df()
print(result.to_string(index=False))
print()

# ---- Step 3: Same file, different interpretation ----
print("Step 3: Same file, different column names, same result")
result = con.execute("""
    SELECT
        product_id AS product,
        amount     AS revenue
    FROM read_csv_auto('sales.csv')
    LIMIT 3
""").df()
print(result.to_string(index=False))
print()

# ---- Step 4: The "metastore" - DuckDB's information_schema ----
print("Step 4: What a metastore holds for a materialized table")
con.execute("CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales.csv')")
meta = con.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'sales'
""").df()
print(meta.to_string(index=False))
print()

# ---- Step 5: Same data, different SerDe (CSV vs JSON) ----
print("Step 5: Same data read through two different SerDes")
csv_count = con.execute(
    "SELECT COUNT(*) FROM read_csv_auto('sales.csv')").fetchone()[0]
json_count = con.execute(
    "SELECT COUNT(*) FROM read_json_auto('sales.json')").fetchone()[0]

print(f"  CSV SerDe:  {csv_count} rows")
print(f"  JSON SerDe: {json_count} rows (subset of the same data)")