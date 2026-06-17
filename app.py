import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="RetailPulse", page_icon="📊", layout="wide")

st.markdown("<h1 style='text-align:center;color:#00BFFF;'>📊 RetailPulse</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#FFA500;'>AI-Powered Retail Analytics Platform</h3>", unsafe_allow_html=True)
st.markdown("---")

summary = pd.read_csv("data/executive_summary.csv")
monthly = pd.read_csv("data/monthly_sales.csv")
country = pd.read_csv("data/country_dashboard.csv")
segments = pd.read_csv("data/customer_segments.csv")
inventory = pd.read_csv("data/inventory_optimization.csv")
forecast = pd.read_csv("data/sales_forecast.csv")
product = pd.read_csv("data/product_performance.csv")
churn = pd.read_csv("data/customer_churn_data.csv")
retail = pd.read_csv("data/cleaned_retail.csv")

dashboard = st.sidebar.radio(
    "📌 Select Dashboard",
    [
        "Executive Summary",
        "Sales Trend Analysis",
        "Product Performance",
        "Customer Analytics",
        "Region/Country Sales",
        "Monthly & Seasonal Sales",
        "Customer Behaviour",
        "Profit & Revenue Analysis",
        "Inventory Risk Dashboard",
        "Order & Transaction Dashboard",
        "Advanced Analytics Dashboard",
        "Interactive Filter Dashboard"
    ]
)

if dashboard == "Executive Summary":
    st.subheader("Executive Summary Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    try:
        c1.metric("Customers", int(summary.loc[summary['Metric']=="Total Customers",'Value'].values[0]))
        c2.metric("Products", int(summary.loc[summary['Metric']=="Total Products",'Value'].values[0]))
        c3.metric("High Risk Products", int(summary.loc[summary['Metric']=="High Risk Products",'Value'].values[0]))
        c4.metric("Churned Customers", int(summary.loc[summary['Metric']=="Churned Customers",'Value'].values[0]))
    except:
        st.dataframe(summary)

elif dashboard == "Sales Trend Analysis":
    st.subheader("Sales Trend Analysis Dashboard")
    st.plotly_chart(px.line(monthly,x="Month",y="TotalAmount",markers=True),use_container_width=True)

elif dashboard == "Product Performance":
    st.subheader("Product Performance Dashboard")
    top_products = product.sort_values("TotalAmount",ascending=False).head(10)
    st.plotly_chart(px.bar(top_products,x="Description",y="TotalAmount",color="TotalAmount"),use_container_width=True)
    st.dataframe(top_products)

elif dashboard == "Customer Analytics":
    st.subheader("Customer Analytics Dashboard")
    st.plotly_chart(px.pie(segments,names="Segment"),use_container_width=True)
    st.dataframe(segments.head(20))

elif dashboard == "Region/Country Sales":
    st.subheader("Region/Country Sales Dashboard")
    st.plotly_chart(px.bar(country.sort_values("TotalAmount",ascending=False),x="Country",y="TotalAmount",color="TotalAmount"),use_container_width=True)

elif dashboard == "Monthly & Seasonal Sales":
    st.subheader("Monthly & Seasonal Sales Dashboard")
    st.plotly_chart(px.bar(monthly,x="Month",y="TotalAmount",color="TotalAmount"),use_container_width=True)

elif dashboard == "Customer Behaviour":
    st.subheader("Customer Behaviour Dashboard")
    a,b,c = st.columns(3)
    with a: st.plotly_chart(px.histogram(segments,x="Recency"),use_container_width=True)
    with b: st.plotly_chart(px.histogram(segments,x="Frequency"),use_container_width=True)
    with c: st.plotly_chart(px.histogram(segments,x="Monetary"),use_container_width=True)

elif dashboard == "Profit & Revenue Analysis":
    st.subheader("Profit & Revenue Analysis Dashboard")
    revenue_country = retail.groupby("Country")["TotalAmount"].sum().reset_index()
    st.plotly_chart(px.bar(revenue_country.sort_values("TotalAmount",ascending=False).head(10),x="Country",y="TotalAmount"),use_container_width=True)

elif dashboard == "Inventory Risk Dashboard":
    st.subheader("Inventory Risk Dashboard")
    st.plotly_chart(px.pie(inventory,names="InventoryStatus"),use_container_width=True)
    st.dataframe(inventory.sort_values("ReorderQuantity",ascending=False).head(10))

elif dashboard == "Order & Transaction Dashboard":
    st.subheader("Order & Transaction Dashboard")
    order_count = retail.groupby("Month")["Invoice"].count().reset_index()
    st.plotly_chart(px.line(order_count,x="Month",y="Invoice",markers=True),use_container_width=True)
    st.metric("Total Transactions", retail["Invoice"].nunique())

elif dashboard == "Advanced Analytics Dashboard":
    st.subheader("Advanced Analytics Dashboard")
    c1,c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.line(forecast,x="SalesDate",y="PredictedSales"),use_container_width=True)
    with c2:
        churn_count = churn["Churn"].value_counts()
        st.plotly_chart(px.pie(names=["Active","Churn"][:len(churn_count)], values=churn_count.values),use_container_width=True)

elif dashboard == "Interactive Filter Dashboard":
    st.subheader("Interactive Filter Dashboard")
    selected_country = st.selectbox("Select Country", sorted(retail["Country"].dropna().unique()))
    filtered = retail[retail["Country"] == selected_country]
    st.metric("Revenue", round(filtered["TotalAmount"].sum(),2))
    monthly_filtered = filtered.groupby("Month")["TotalAmount"].sum().reset_index()
    st.plotly_chart(px.bar(monthly_filtered,x="Month",y="TotalAmount"),use_container_width=True)
