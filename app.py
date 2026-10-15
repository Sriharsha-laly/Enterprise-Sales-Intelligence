
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import (
    load_data,
    calculate_kpis,
    monthly_trends,
    regional_performance,
    product_performance
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Nexus | Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PROFESSIONAL COLOR THEME
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0B1020 0%, #111827 100%);
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background: #10182B;
        border-right: 1px solid #273449;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(110deg, #312E81, #164E63, #172554);
        border: 1px solid #475569;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: 34px;
        margin-bottom: 4px;
    }

    .hero p {
        color: #CBD5E1;
        margin: 0;
        font-size: 15px;
    }

    .metric-card {
        background: linear-gradient(145deg, #172033, #1E293B);
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #334155;
        min-height: 125px;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 27px;
        font-weight: 750;
    }

    .metric-note {
        color: #22D3EE;
        font-size: 12px;
        margin-top: 7px;
    }

    .section-title {
        color: #E2E8F0;
        font-size: 21px;
        font-weight: 700;
        margin-top: 18px;
    }

    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(90deg, #7C3AED, #0891B2);
        color: white;
        border: 0;
        border-radius: 9px;
    }

    div[data-testid="stMetric"] {
        background: #172033;
        padding: 12px;
        border: 1px solid #334155;
        border-radius: 12px;
    }

    .small-note {
        color: #94A3B8;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def money(value):
    return f"${value:,.0f}"


def metric_card(label, value, note, accent="#22D3EE"):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{accent}">
                {value}
            </div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1"),
        margin=dict(l=15, r=15, t=45, b=15),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def get_data():
    return load_data("data/sales_data.csv")


if not os.path.exists("data/sales_data.csv"):
    st.error("Dataset not found. Run `python generate_data.py` first.")
    st.stop()

try:
    data = get_data()
except Exception as error:
    st.error(f"Could not load sales data: {error}")
    st.stop()

if data.empty:
    st.error("The dataset contains no usable records.")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.markdown("## 📊 NEXUS")
st.sidebar.caption("ENTERPRISE SALES INTELLIGENCE")
st.sidebar.divider()

st.sidebar.markdown("### 🔎 Dashboard Filters")

min_date = data["Order_Date"].min().date()
max_date = data["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

regions = sorted(data["Region"].dropna().unique())
categories = sorted(data["Category"].dropna().unique())
segments = sorted(data["Customer_Segment"].dropna().unique())
channels = sorted(data["Sales_Channel"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Regions",
    regions,
    default=regions
)

selected_categories = st.sidebar.multiselect(
    "Categories",
    categories,
    default=categories
)

selected_segments = st.sidebar.multiselect(
    "Customer segments",
    segments,
    default=segments
)

selected_channels = st.sidebar.multiselect(
    "Sales channels",
    channels,
    default=channels
)

st.sidebar.divider()
st.sidebar.caption("Nexus Portfolio Edition · Sample data")


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered = data.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    if start_date and end_date:
        filtered = filtered[
            filtered["Order_Date"].dt.date.between(
                start_date, end_date
            )
        ]

filtered = filtered[
    filtered["Region"].isin(selected_regions)
    & filtered["Category"].isin(selected_categories)
    & filtered["Customer_Segment"].isin(selected_segments)
    & filtered["Sales_Channel"].isin(selected_channels)
]

if filtered.empty:
    st.warning("No records match these filters. Change your selections.")
    st.stop()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>⚡ NEXUS Sales Intelligence</h1>
    <p>
        Enterprise analytics · Performance monitoring ·
        Revenue insights · Decision support
    </p>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"Showing {len(filtered):,} transactions from "
    f"{filtered['Order_Date'].min():%d %b %Y} to "
    f"{filtered['Order_Date'].max():%d %b %Y}"
)


# --------------------------------------------------
# EXECUTIVE KPI CARDS
# --------------------------------------------------
kpis = calculate_kpis(filtered)

st.markdown('<div class="section-title">Executive Overview</div>',
            unsafe_allow_html=True)
st.write("")

cols = st.columns(4)

with cols[0]:
    metric_card(
        "TOTAL REVENUE",
        money(kpis["revenue"]),
        "Revenue after recorded discounts",
        "#22D3EE"
    )

with cols[1]:
    metric_card(
        "TOTAL PROFIT",
        money(kpis["profit"]),
        "Revenue minus recorded cost",
        "#A78BFA"
    )

with cols[2]:
    metric_card(
        "PROFIT MARGIN",
        f"{kpis['profit_margin']:.1f}%",
        "Profit / revenue",
        "#34D399"
    )

with cols[3]:
    metric_card(
        "TRANSACTIONS",
        f"{kpis['orders']:,}",
        f"{kpis['completed_orders']:,} completed",
        "#FBBF24"
    )

st.write("")
cols = st.columns(3)

with cols[0]:
    st.metric(
        "Average completed order",
        money(kpis["average_order_value"])
    )

with cols[1]:
    st.metric(
        "Recorded return rate",
        f"{kpis['return_rate']:.1f}%"
    )

with cols[2]:
    st.metric(
        "Total recorded cost",
        money(kpis["cost"])
    )


# --------------------------------------------------
# MONTHLY REVENUE AND PROFIT
# --------------------------------------------------
st.markdown('<div class="section-title">📈 Revenue & Profit Trends</div>',
            unsafe_allow_html=True)

monthly = monthly_trends(filtered)

left, right = st.columns(2)

with left:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(color="#22D3EE", width=3),
        fill="tozeroy",
        fillcolor="rgba(34,211,238,0.10)"
    ))
    fig.update_layout(
        title="Monthly Revenue",
        xaxis_title="Month",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with right:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["Month"],
        y=monthly["Profit"],
        name="Profit",
        marker_color="#A78BFA"
    ))
    fig.update_layout(
        title="Monthly Profit",
        xaxis_title="Month",
        yaxis_title="Profit ($)"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)


# --------------------------------------------------
# REGIONAL AND CATEGORY ANALYSIS
# --------------------------------------------------
st.markdown('<div class="section-title">🌍 Business Performance</div>',
            unsafe_allow_html=True)

left, right = st.columns(2)

region_data = regional_performance(filtered)
category_data = (
    filtered.groupby("Category", as_index=False)
    .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    .sort_values("Revenue", ascending=False)
)

with left:
    fig = px.bar(
        region_data,
        x="Region",
        y="Revenue",
        color="Profit",
        color_continuous_scale=["#7C3AED", "#22D3EE"],
        title="Revenue by Region",
        hover_data=["Profit", "Orders"]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with right:
    fig = px.pie(
        category_data,
        names="Category",
        values="Revenue",
        hole=0.55,
        title="Revenue Share by Category",
        color_discrete_sequence=[
            "#22D3EE", "#A78BFA", "#34D399", "#FBBF24"
        ]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)


# --------------------------------------------------
# PRODUCT PROFITABILITY
# --------------------------------------------------
st.markdown('<div class="section-title">🏆 Product Intelligence</div>',
            unsafe_allow_html=True)

products = product_performance(filtered)

left, right = st.columns(2)

with left:
    fig = px.bar(
        products.sort_values("Profit", ascending=True),
        x="Profit",
        y="Product",
        orientation="h",
        title="Products Ranked by Profit",
        color="Profit",
        color_continuous_scale=["#F87171", "#34D399"],
        hover_data=["Revenue", "Quantity", "Profit_Margin"]
    )
    st.plotly_chart(style_chart(fig, 400), use_container_width=True)

with right:
    fig = px.scatter(
        filtered,
        x="Discount",
        y="Profit",
        size="Revenue",
        color="Category",
        hover_name="Product",
        title="Discount vs Profit",
        labels={
            "Discount": "Discount rate",
            "Profit": "Profit ($)"
        }
    )
    fig.update_xaxes(tickformat=".0%")
    st.plotly_chart(style_chart(fig, 400), use_container_width=True)

st.dataframe(
    products.style.format({
        "Revenue": "${:,.2f}",
        "Profit": "${:,.2f}",
        "Profit_Margin": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# CUSTOMER AND CHANNEL INTELLIGENCE
# --------------------------------------------------
st.markdown('<div class="section-title">👥 Customer & Channel Intelligence</div>',
            unsafe_allow_html=True)

left, right = st.columns(2)

segment_data = (
    filtered.groupby("Customer_Segment", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
)

channel_data = (
    filtered.groupby("Sales_Channel", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
)

with left:
    fig = px.bar(
        segment_data,
        x="Customer_Segment",
        y="Revenue",
        color="Customer_Segment",
        title="Revenue by Customer Segment",
        color_discrete_sequence=["#22D3EE", "#A78BFA", "#34D399"]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with right:
    fig = px.bar(
        channel_data,
        x="Sales_Channel",
        y="Revenue",
        color="Sales_Channel",
        title="Revenue by Sales Channel",
        color_discrete_sequence=["#A78BFA", "#22D3EE", "#FBBF24"]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)


# --------------------------------------------------
# SIMPLE REVENUE FORECAST
# --------------------------------------------------
st.markdown('<div class="section-title">🔮 Revenue Forecast</div>',
            unsafe_allow_html=True)

st.caption(
    "Illustrative linear trend projection based on monthly revenue. "
    "This is not a validated predictive model."
)

if len(monthly) >= 3:
    y = monthly["Revenue"].astype(float).to_numpy()
    x = np.arange(len(y), dtype=float)

    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(len(y), len(y) + 3, dtype=float)
    forecast = slope * future_x + intercept
    forecast = np.maximum(forecast, 0)

    last_month = pd.Period(monthly["Month"].iloc[-1], freq="M")
    future_months = [
        str(last_month + i) for i in range(1, 4)
    ]

    forecast_df = pd.DataFrame({
        "Month": future_months,
        "Forecast_Revenue": forecast
    })

    historical_df = monthly[["Month", "Revenue"]].copy()
    historical_df = historical_df.rename(
        columns={"Revenue": "Forecast_Revenue"}
    )
    historical_df["Type"] = "Historical"

    forecast_df["Type"] = "Forecast"

    combined = pd.concat(
        [historical_df, forecast_df],
        ignore_index=True
    )

    fig = px.line(
        combined,
        x="Month",
        y="Forecast_Revenue",
        color="Type",
        markers=True,
        title="Historical Revenue and Next 3 Months",
        color_discrete_map={
            "Historical": "#22D3EE",
            "Forecast": "#FBBF24"
        }
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.dataframe(
        forecast_df[["Month", "Forecast_Revenue"]].style.format({
            "Forecast_Revenue": "${:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("At least three months of data are needed for this forecast.")


# --------------------------------------------------
# AUTOMATED BUSINESS ALERTS
# --------------------------------------------------
st.markdown('<div class="section-title">🚨 Business Alerts</div>',
            unsafe_allow_html=True)

alerts = []

if kpis["profit_margin"] < 10:
    alerts.append(
        ("warning", "Low overall profit margin",
         f"Current margin is {kpis['profit_margin']:.1f}%. Review pricing and costs.")
    )

if kpis["return_rate"] > 8:
    alerts.append(
        ("warning", "High recorded return rate",
         f"Return rate is {kpis['return_rate']:.1f}%. Investigate product quality and return reasons.")
    )

if not products.empty:
    low_profit = products.sort_values("Profit").iloc[0]
    alerts.append(
        ("info", "Lowest-profit product in this selection",
         f"{low_profit['Product']} has recorded profit of {money(low_profit['Profit'])}.")
    )

if not alerts:
    st.success("No alerts triggered by the current simple rules.")

for level, title, message in alerts:
    if level == "warning":
        st.warning(f"**{title}:** {message}")
    else:
        st.info(f"**{title}:** {message}")


# --------------------------------------------------
# TRANSACTION EXPLORER AND EXPORT
# --------------------------------------------------
st.markdown('<div class="section-title">🔍 Transaction Explorer</div>',
            unsafe_allow_html=True)

search = st.text_input(
    "Search by order ID or product",
    placeholder="Example: ORD-00010 or Laptop"
)

transactions = filtered.copy()

if search.strip():
    mask = (
        transactions["Order_ID"].astype(str).str.contains(
            search, case=False, na=False
        )
        | transactions["Product"].astype(str).str.contains(
            search, case=False, na=False
        )
    )
    transactions = transactions[mask]

st.caption(f"{len(transactions):,} matching records")

st.dataframe(
    transactions.sort_values("Order_Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="⬇️ Download filtered transactions (CSV)",
    data=transactions.to_csv(index=False).encode("utf-8"),
    file_name="nexus_filtered_sales.csv",
    mime="text/csv"
)

st.download_button(
    label="⬇️ Download product performance (CSV)",
    data=products.to_csv(index=False).encode("utf-8"),
    file_name="nexus_product_performance.csv",
    mime="text/csv"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown(
    """
    <p class="small-note">
        NEXUS Sales Intelligence · Data Analyst Portfolio Project<br>
        Sample dataset for demonstration only. Forecasts and alerts are
        illustrative and should be validated before business use.
    </p>
    """,
    unsafe_allow_html=True
)