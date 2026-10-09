"""
Retail Sales & Profit Analytics Dashboard
Run: streamlit run project.py
This project uses a reproducible synthetic retail dataset generated in code.
No external data download is required.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Retail Sales & Profit Analytics", page_icon="📊", layout="wide")

@st.cache_data
def create_data(n: int = 1800, seed: int = 42) -> pd.DataFrame:
    """Create a reproducible demonstration dataset; figures are illustrative, not real company data."""
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2024-01-01")
    days = rng.integers(0, 730, size=n)
    dates = start + pd.to_timedelta(days, unit="D")
    regions = np.array(["North", "South", "East", "West", "Central"])
    categories = np.array(["Electronics", "Home & Kitchen", "Office Supplies", "Furniture", "Accessories"])
    products = {
        "Electronics": ["Headphones", "Keyboard", "Monitor", "Smart Speaker"],
        "Home & Kitchen": ["Cookware Set", "Mixer", "Storage Box", "Water Bottle"],
        "Office Supplies": ["Notebook", "Pen Set", "Printer Paper", "Desk Organizer"],
        "Furniture": ["Office Chair", "Bookshelf", "Study Desk", "Lamp"],
        "Accessories": ["Laptop Bag", "USB Hub", "Mouse Pad", "Phone Stand"],
    }
    category = rng.choice(categories, size=n, p=[.24, .22, .20, .16, .18])
    product = [rng.choice(products[c]) for c in category]
    unit_price = np.array([
        rng.uniform(800, 28000) if c == "Electronics" else
        rng.uniform(150, 6500) if c == "Home & Kitchen" else
        rng.uniform(30, 1800) if c == "Office Supplies" else
        rng.uniform(1200, 16000) if c == "Furniture" else
        rng.uniform(100, 4000)
        for c in category
    ])
    quantity = rng.integers(1, 8, size=n)
    discount = rng.choice([0, .05, .10, .15, .20, .25], size=n, p=[.35, .15, .20, .12, .12, .06])
    revenue = unit_price * quantity * (1 - discount)
    cost_ratio = rng.uniform(.52, .88, size=n)
    profit = revenue * (1 - cost_ratio) - revenue * discount * .15
    region = rng.choice(regions, size=n)
    channel = rng.choice(["Online", "Store", "Partner"], size=n, p=[.52, .33, .15])
    customer_id = [f"C{v:04d}" for v in rng.integers(1, 451, size=n)]
    df = pd.DataFrame({
        "Order_Date": dates, "Order_ID": [f"ORD{v:06d}" for v in range(1, n+1)],
        "Customer_ID": customer_id, "Region": region, "Category": category,
        "Product": product, "Channel": channel, "Quantity": quantity,
        "Unit_Price_INR": unit_price.round(2), "Discount": discount,
        "Revenue_INR": revenue.round(2), "Profit_INR": profit.round(2)
    })
    return df.sort_values("Order_Date").reset_index(drop=True)

df = create_data()
st.title("📊 Retail Sales & Profit Analytics Dashboard")
st.caption("Decision-support demo | Synthetic data generated in-app | Currency: INR")
st.info("Important: This is a demonstration dataset, not actual company data. Use a permitted, non-training dataset if your submission requires a real external source.")

with st.sidebar:
    st.header("Filters")
    min_date, max_date = df["Order_Date"].min().date(), df["Order_Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions_selected = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    categories_selected = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    channels_selected = st.multiselect("Sales channel", sorted(df["Channel"].unique()), default=sorted(df["Channel"].unique()))

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["Order_Date"].dt.date.between(date_range[0], date_range[1])]
filtered = filtered[
    filtered["Region"].isin(regions_selected) &
    filtered["Category"].isin(categories_selected) &
    filtered["Channel"].isin(channels_selected)
]

if filtered.empty:
    st.warning("No records match these filters. Change one or more filters.")
    st.stop()

revenue = filtered["Revenue_INR"].sum()
profit = filtered["Profit_INR"].sum()
orders = filtered["Order_ID"].nunique()
customers = filtered["Customer_ID"].nunique()
aov = revenue / orders if orders else 0
margin = profit / revenue * 100 if revenue else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Revenue", f"₹{revenue:,.0f}")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Unique customers", f"{customers:,}")
c5.metric("Profit margin", f"{margin:.1f}%")
st.caption(f"Average order value: ₹{aov:,.0f} | Records in view: {len(filtered):,}")

tab1, tab2, tab3 = st.tabs(["Executive Overview", "Sales & Products", "Customer & Risk"])

with tab1:
    monthly = filtered.assign(Month=filtered["Order_Date"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False).agg(
        Revenue_INR=("Revenue_INR", "sum"), Profit_INR=("Profit_INR", "sum"), Orders=("Order_ID", "nunique"))
    left, right = st.columns(2)
    with left:
        st.subheader("Monthly revenue trend")
        st.plotly_chart(px.line(monthly, x="Month", y="Revenue_INR", markers=True, title="Revenue by month"), use_container_width=True)
    with right:
        st.subheader("Revenue by region")
        region_summary = filtered.groupby("Region", as_index=False).agg(Revenue_INR=("Revenue_INR","sum"), Profit_INR=("Profit_INR","sum"))
        st.plotly_chart(px.bar(region_summary, x="Region", y="Revenue_INR", color="Profit_INR", title="Revenue and profit by region"), use_container_width=True)
    st.subheader("Business interpretation")
    best_region = region_summary.sort_values("Revenue_INR", ascending=False).iloc[0]
    weakest_margin = (filtered.groupby("Category").agg(revenue=("Revenue_INR","sum"), profit=("Profit_INR","sum")).assign(margin=lambda x: x.profit / x.revenue * 100).sort_values("margin").iloc[0])
    st.write(f"- **Top revenue region in the current selection:** {best_region['Region']} (₹{best_region['Revenue_INR']:,.0f}).")
    st.write(f"- **Category to review for margin:** {weakest_margin.name} ({weakest_margin['margin']:.1f}% estimated margin).")
    st.write("- Compare trends over time before changing budgets; the generated data is illustrative.")

with tab2:
    left, right = st.columns(2)
    cat_summary = filtered.groupby("Category", as_index=False).agg(Revenue_INR=("Revenue_INR","sum"), Profit_INR=("Profit_INR","sum"), Units=("Quantity","sum"))
    with left:
        st.plotly_chart(px.bar(cat_summary.sort_values("Revenue_INR", ascending=False), x="Category", y="Revenue_INR", title="Revenue by category"), use_container_width=True)
    with right:
        st.plotly_chart(px.scatter(filtered, x="Revenue_INR", y="Profit_INR", color="Category", hover_data=["Product","Region"], title="Order revenue vs profit"), use_container_width=True)
    st.subheader("Category summary")
    st.dataframe(cat_summary.sort_values("Revenue_INR", ascending=False).style.format({"Revenue_INR":"₹{:,.0f}","Profit_INR":"₹{:,.0f}","Units":"{:,.0f}"}), use_container_width=True)
    st.download_button("Download filtered data (CSV)", filtered.to_csv(index=False).encode("utf-8"), "filtered_retail_data.csv", "text/csv")

with tab3:
    customer = filtered.groupby("Customer_ID", as_index=False).agg(Orders=("Order_ID","nunique"), Revenue_INR=("Revenue_INR","sum"), Profit_INR=("Profit_INR","sum"), Last_Order=("Order_Date","max"))
    customer["Days_Since_Order"] = (filtered["Order_Date"].max() - customer["Last_Order"]).dt.days
    customer["Risk_Flag"] = np.where(customer["Days_Since_Order"] >= 180, "Review: inactive 180+ days", "Active in last 180 days")
    risk_count = (customer["Days_Since_Order"] >= 180).sum()
    col1, col2 = st.columns(2)
    col1.metric("Customers inactive 180+ days", f"{risk_count:,}")
    col2.metric("Share flagged", f"{risk_count / len(customer) * 100:.1f}%")
    st.plotly_chart(px.histogram(customer, x="Days_Since_Order", nbins=20, title="Customer recency distribution"), use_container_width=True)
    st.subheader("Customers for review")
    st.dataframe(customer.sort_values(["Days_Since_Order","Revenue_INR"], ascending=[False,False]).head(25), use_container_width=True)
    st.write("**Suggested action:** Review high-value customers with long gaps since their last order and test a targeted retention offer. Validate this hypothesis with real business data before acting.")

with st.expander("Methodology, definitions and limitations"):
    st.markdown("""
    - **Revenue:** sum of discounted order line revenue.
    - **Profit:** illustrative estimated profit after a simulated cost ratio and a small discount penalty.
    - **Average order value:** revenue divided by distinct order IDs.
    - **Customer inactivity flag:** no order within 180 days of the latest date in the filtered data.
    - This dataset is synthetic and generated with a fixed random seed for reproducibility. Results should not be presented as real-world findings.
    - The current version is descriptive analytics; no forecast or causal claim is made.
    """)
