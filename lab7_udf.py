# lab7_udf.py - UDF demonstration using Python and DuckDB
import duckdb

con = duckdb.connect()

# Define a Python function for customer tax tier tagging
def categorize_tier(amount):
    if amount > 5000:
        return "PLATINUM"
    elif amount > 1000:
        return "GOLD"
    else:
        return "SILVER"

# Register the Python function as a UDF in DuckDB
con.create_function("categorize_tier", categorize_tier, ["DOUBLE"], "VARCHAR")

# Use UDF in a HiveQL-style SELECT statement
result = con.execute("""
    SELECT 
        sale_id,
        amount,
        categorize_tier(amount) AS tier
    FROM read_csv_auto('sales.csv')
    LIMIT 10
""").df()

print("--- UDF Tier Classification Output ---")
print(result.to_string(index=False))