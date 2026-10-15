
import pandas as pd


def load_data(path="data/sales_data.csv"):
    """Load and validate the sales dataset."""
    df = pd.read_csv(path, parse_dates=["Order_Date"])

    required_columns = [
        "Order_ID", "Order_Date", "Region", "Category",
        "Product", "Customer_Segment", "Sales_Channel",
        "Quantity", "Unit_Price", "Discount",
        "Revenue", "Cost", "Profit", "Order_Status"
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df = df.drop_duplicates(subset=["Order_ID"]).copy()

    numeric_columns = [
        "Quantity", "Unit_Price", "Discount",
        "Revenue", "Cost", "Profit"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(
        subset=["Order_Date", "Revenue", "Cost", "Profit"]
    )

    return df


def calculate_kpis(df):
    """Calculate headline business metrics."""
    revenue = df["Revenue"].sum()
    profit = df["Profit"].sum()
    cost = df["Cost"].sum()

    completed = df[df["Order_Status"] == "Completed"]
    total_orders = len(df)
    completed_orders = len(completed)

    return {
        "revenue": float(revenue),
        "profit": float(profit),
        "cost": float(cost),
        "orders": int(total_orders),
        "completed_orders": int(completed_orders),
        "average_order_value": (
            float(completed["Revenue"].mean())
            if completed_orders else 0.0
        ),
        "profit_margin": (
            float(profit / revenue * 100)
            if revenue else 0.0
        ),
        "return_rate": (
            float((df["Order_Status"] == "Returned").mean() * 100)
            if total_orders else 0.0
        )
    }


def monthly_trends(df):
    """Aggregate sales by calendar month."""
    result = df.copy()
    result["Month"] = result["Order_Date"].dt.to_period("M").astype(str)

    return (
        result.groupby("Month", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .sort_values("Month")
    )


def regional_performance(df):
    """Compare business performance by region."""
    return (
        df.groupby("Region", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .sort_values("Revenue", ascending=False)
    )


def product_performance(df):
    """Rank products by revenue and profitability."""
    result = (
        df.groupby("Product", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order_ID", "nunique")
        )
    )

    result["Profit_Margin"] = (
        result["Profit"] / result["Revenue"].replace(0, float("nan")) * 100
    ).fillna(0)

    return result.sort_values("Profit", ascending=False)