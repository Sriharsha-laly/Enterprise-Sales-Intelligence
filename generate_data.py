
import os
import numpy as np
import pandas as pd

# Reproducible sample data
np.random.seed(42)

os.makedirs("data", exist_ok=True)

n = 3000

dates = pd.date_range(
    start="2024-01-01",
    end="2026-09-30",
    freq="D"
)

products = {
    "Laptop": (850, 1500),
    "Smartphone": (350, 1000),
    "Headphones": (30, 180),
    "Monitor": (150, 500),
    "Keyboard": (20, 120),
    "Tablet": (200, 700),
    "Smartwatch": (100, 400),
    "Accessories": (10, 90)
}

product_names = list(products.keys())
selected_products = np.random.choice(product_names, n)

rows = []

for i in range(n):
    product = selected_products[i]
    low, high = products[product]

    price = round(np.random.uniform(low, high), 2)
    quantity = int(np.random.randint(1, 8))
    discount = round(np.random.choice(
        [0, 0.05, 0.10, 0.15, 0.20, 0.25],
        p=[0.25, 0.15, 0.25, 0.15, 0.15, 0.05]
    ), 2)

    revenue = round(price * quantity * (1 - discount), 2)
    cost = round(price * quantity * np.random.uniform(0.48, 0.78), 2)
    profit = round(revenue - cost, 2)

    order_date = np.random.choice(dates)
    status = np.random.choice(
        ["Completed", "Returned", "Cancelled"],
        p=[0.90, 0.06, 0.04]
    )

    if status == "Returned":
        revenue = 0.0
        profit = round(-cost, 2)
    elif status == "Cancelled":
        revenue = 0.0
        profit = 0.0

    rows.append({
        "Order_ID": f"ORD-{i + 1:05d}",
        "Order_Date": pd.Timestamp(order_date),
        "Region": np.random.choice(
            ["North", "South", "East", "West", "Central"]
        ),
        "Category": np.random.choice(
            ["Electronics", "Accessories", "Computing"]
        ),
        "Product": product,
        "Customer_Segment": np.random.choice(
            ["Consumer", "Corporate", "Small Business"]
        ),
        "Sales_Channel": np.random.choice(
            ["Online", "Retail Store", "Partner"]
        ),
        "Quantity": quantity,
        "Unit_Price": price,
        "Discount": discount,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "Order_Status": status
    })

df = pd.DataFrame(rows)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df = df.sort_values("Order_Date").reset_index(drop=True)

output_path = "data/sales_data.csv"
df.to_csv(output_path, index=False)

print("Sales dataset created successfully!")
print(f"File: {output_path}")
print(f"Total transactions: {len(df):,}")
print(f"Revenue: ${df['Revenue'].sum():,.2f}")
print(f"Profit: ${df['Profit'].sum():,.2f}")