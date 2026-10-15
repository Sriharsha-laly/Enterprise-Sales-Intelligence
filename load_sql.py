
import os
import sqlite3
import pandas as pd

CSV_PATH = "data/sales_data.csv"
DB_PATH = "sales_intelligence.db"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        "Dataset not found. Run: python generate_data.py"
    )

df = pd.read_csv(CSV_PATH, parse_dates=["Order_Date"])

with sqlite3.connect(DB_PATH) as connection:
    df.to_sql(
        "sales_data",
        connection,
        if_exists="replace",
        index=False
    )

    count = pd.read_sql_query(
        "SELECT COUNT(*) AS total_rows FROM sales_data",
        connection
    ).iloc[0]["total_rows"]

print("SQLite database created successfully!")
print(f"Database: {DB_PATH}")
print(f"Rows stored: {count:,}")

with sqlite3.connect(DB_PATH) as connection:
    summary = pd.read_sql_query(
        """
        SELECT
            Region,
            ROUND(SUM(Revenue), 2) AS Total_Revenue,
            ROUND(SUM(Profit), 2) AS Total_Profit,
            COUNT(*) AS Total_Orders
        FROM sales_data
        GROUP BY Region
        ORDER BY Total_Revenue DESC
        """,
        connection
    )

print("\nRegional SQL summary:")
print(summary.to_string(index=False))