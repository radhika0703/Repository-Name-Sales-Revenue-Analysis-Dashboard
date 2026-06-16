import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------
# Page Config
# --------------------
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("Analyze sales, profit, and product performance.")

# --------------------
# Load Data
# --------------------
# --------------------
# Load Data
# --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore.csv", encoding="latin1")
    return df

df = load_data()

st.write("Columns in Dataset:")
st.write(df.columns.tolist())

# --------------------
# Data Cleaning
# --------------------
df["Order.Date"] = pd.to_datetime(df["Order.Date"])

# --------------------
# Sidebar Filters
# --------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

# --------------------
# KPI Metrics
# --------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order.ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"${total_sales:,.0f}")
c2.metric("Total Profit", f"${total_profit:,.0f}")
c3.metric("Orders", total_orders)
c4.metric("Units Sold", f"{total_quantity:,}")

st.divider()

# --------------------
# Monthly Revenue Trend
# --------------------
filtered_df["Month"] = (
    filtered_df["Order.Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------
# Sales by Category
# --------------------
category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------
# Sales by Region
# --------------------
region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Revenue Distribution by Region"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------
# Top 10 Products
# --------------------
top_products = (
    filtered_df.groupby("Product.Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product.Name",
    orientation="h",
    title="Top 10 Products by Revenue"
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------
# Profit by Category
# --------------------
profit_category = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    profit_category,
    x="Category",
    y="Profit",
    title="Profit by Category"
)

st.plotly_chart(fig5, use_container_width=True)

# --------------------
# Data Preview
# --------------------
st.subheader("Dataset Preview")

st.dataframe(filtered_df)

# --------------------
# Download Report
# --------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Report",
    csv,
    "sales_report.csv",
    "text/csv"
)