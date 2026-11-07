# lab5_hiveql.py - HiveQL-style analytics with DuckDB
import duckdb

con = duckdb.connect()

# Create view abstractions over CSV files
con.execute("CREATE VIEW sales AS SELECT * FROM read_csv_auto('sales.csv')")
con.execute("CREATE VIEW products AS SELECT * FROM read_csv_auto('products.csv')")
con.execute("CREATE VIEW stores AS SELECT * FROM read_csv_auto('stores.csv')")

print("--- Query 1: Top 5 Product Categories by Revenue ---")
q1 = con.execute("""
    SELECT 
        p.category,
        COUNT(s.sale_id) AS total_sales,
        SUM(s.amount)    AS total_revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
""").df()
print(q1.to_string(index=False))
print()

print("--- Query 2: Regional Performance Summary ---")
q2 = con.execute("""
    SELECT 
        st.region,
        COUNT(DISTINCT st.store_id) AS store_count,
        SUM(s.amount)               AS regional_revenue
    FROM sales s
    JOIN stores st ON s.store_id = st.store_id
    GROUP BY st.region
    ORDER BY regional_revenue DESC
""").df()
print(q2.to_string(index=False))
print()

print("--- Query 3: Monthly Sales View ---")
con.execute("""
    CREATE VIEW monthly_sales_summary AS
    SELECT 
        STRFTIME(CAST(dt AS DATE), '%Y-%m') AS month,
        COUNT(*) AS total_transactions,
        SUM(amount) AS total_revenue
    FROM sales
    GROUP BY month
""")

q3 = con.execute("SELECT * FROM monthly_sales_summary ORDER BY month").df()
print(q3.to_string(index=False))