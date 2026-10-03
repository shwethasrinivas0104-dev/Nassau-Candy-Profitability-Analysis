import pandas as pd

df = pd.read_csv("Nassau Candy Distributor.csv")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y"
)

print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nFirst 5 Rows:")
print(df.head())

print("\nNumerical Summary:")
print(df.describe())

print("\nMinimum Values:")
print(df[["Sales", "Units", "Gross Profit", "Cost"]].min())

print("\nMaximum Values:")
print(df[["Sales", "Units", "Gross Profit", "Cost"]].max())

print("\nNegative Values:")
print((df[["Sales", "Units", "Gross Profit", "Cost"]] < 0).sum())

df["Profit Margin"] = (df["Gross Profit"] / df["Sales"]) * 100

print("\nProfit Margin:")
print(df[["Sales", "Gross Profit", "Profit Margin"]].head())


df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month

print("\nYear and Month:")
print(df[["Order Date", "Order Year", "Order Month"]].head())

print("\nShip Modes:")
print(df["Ship Mode"].unique())

print("\nRegions:")
print(df["Region"].unique())

print("\nDivisions:")
print(df["Division"].unique())

print("\nNumber of Products:")
print(df["Product Name"].nunique())

print("\nProfit by Division:")

division_profit = df.groupby("Division")["Gross Profit"].sum()

print(division_profit)

print("\nProfit by Product:")

product_profit = df.groupby("Product Name")["Gross Profit"].sum()

print(product_profit.sort_values(ascending=False).head(10))

print("\nSales by Region:")

region_sales = df.groupby("Region")["Sales"].sum()

print(region_sales.sort_values(ascending=False))

print("\nProfit by Region:")

region_profit = df.groupby("Region")["Gross Profit"].sum()

print(region_profit.sort_values(ascending=False))

print("\nSales by Division:")

division_sales = df.groupby("Division")["Sales"].sum()

print(division_sales.sort_values(ascending=False))

print("\nProfit by Division:")
print(df.groupby("Division")["Gross Profit"].sum().sort_values(ascending=False))

print("\nProfit by Product:")

product_profit = df.groupby("Product Name")["Gross Profit"].sum()

print(product_profit.sort_values(ascending=False))

print("\nProfit per Unit:")

df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

print(
    df.groupby("Product Name")["Profit per Unit"]
    .mean()
    .sort_values(ascending=False)
)
print("\nProfit per Unit:")

df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

print(df.groupby("Product Name")["Profit per Unit"].mean().sort_values(ascending=False))

print("\nRevenue Contribution:")

product_sales = df.groupby("Product Name")["Sales"].sum()

revenue_contribution = (product_sales / df["Sales"].sum()) * 100

print(revenue_contribution.sort_values(ascending=False))

print("\nMargin Volatility:")

margin_volatility = (
    df.groupby("Product Name")["Profit Margin"]
    .std()
    .sort_values(ascending=False)
)

print(margin_volatility)
print("\nCost vs Sales:")

print(df[["Product Name", "Sales", "Cost"]].head(10))

margin_threshold = 20
print("\nMargin Risk Flags:")

df["Margin Risk"] = df["Profit Margin"].apply(
    lambda x: "High Risk" if x < margin_threshold else "Normal"
)


print(df[["Product Name", "Profit Margin", "Margin Risk"]].head(10))

import streamlit as st
st.title("Nassau Candy Profitability Analysis")

st.subheader("Key Performance Indicators")
division_filter = st.selectbox(
    "Select Division",
    ["All"] + sorted(df["Division"].unique().tolist())
)

start_date, end_date = st.date_input(
    "Select Date Range",
    [df["Order Date"].min().date(), df["Order Date"].max().date()]
)

df = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date)
]
if division_filter != "All":
    df = df[df["Division"] == division_filter]
product_search = st.text_input("Search Product")

if product_search:
    df = df[
        df["Product Name"].str.contains(
            product_search,
            case=False,
            na=False
        )
    ]    

df["Margin Risk"] = df["Profit Margin"].apply(
    lambda x: "High Risk" if x < margin_threshold else "Normal"
)

col1, col2, col3 = st.columns(3)


col1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
col2.metric("Total Gross Profit", f"${df['Gross Profit'].sum():,.2f}")
col3.metric("Average Profit Margin", f"{df['Profit Margin'].mean():.2f}%")

st.subheader("Product Profitability")

product_summary = df.groupby("Product Name").agg({
    "Sales": "sum",
    "Gross Profit": "sum",
    "Profit Margin": "mean"
}).reset_index()

st.dataframe(product_summary)

st.subheader("Division Performance")

division_summary = df.groupby("Division").agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

st.dataframe(division_summary)

st.subheader("Revenue vs Profit")

st.bar_chart(
    division_summary.set_index("Division")[["Sales", "Gross Profit"]]
)
st.subheader("Profit Margin by Product")

st.bar_chart(
    product_summary.set_index("Product Name")["Profit Margin"]
)
margin_threshold = st.slider(
    "Margin Threshold (%)",
    min_value=0,
    max_value=100,
    value=20
)
st.subheader("Margin Risk Flags")

product_summary["Margin Risk"] = product_summary["Profit Margin"].apply(
    lambda x: "High Risk" if x < margin_threshold else "Normal"
)

risk_products = product_summary[
    product_summary["Profit Margin"] < margin_threshold
]

st.dataframe(
    risk_products[
        ["Product Name", "Sales", "Gross Profit", "Profit Margin", "Margin Risk"]
    ]
)

