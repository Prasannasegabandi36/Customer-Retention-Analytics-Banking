import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Bank Customer Retention Analytics",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank.csv")
    return df

df = load_data()

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------
df["Engagement_Profile"] = np.select(
    [
        (df["IsActiveMember"] == 1) & (df["NumOfProducts"] >= 2),
        (df["IsActiveMember"] == 0) & (df["Balance"] > 100000),
        (df["IsActiveMember"] == 1) & (df["NumOfProducts"] == 1),
        (df["IsActiveMember"] == 0)
    ],
    [
        "Active Engaged Customer",
        "Inactive High-Balance Customer",
        "Active Low-Product Customer",
        "Inactive Disengaged Customer"
    ],
    default="Other Customer"
)

df["Relationship_Strength_Index"] = (
    np.where(df["IsActiveMember"] == 1, 1, 0) +
    np.where(df["NumOfProducts"] >= 2, 1, 0) +
    np.where(df["HasCrCard"] == 1, 1, 0) +
    np.where(df["Tenure"] >= 5, 1, 0)
)

df["Relationship_Category"] = pd.cut(
    df["Relationship_Strength_Index"],
    bins=[-1, 1, 2, 4],
    labels=["Weak Relationship", "Medium Relationship", "Strong Relationship"]
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.title("🔍 Filters")

geography = st.sidebar.multiselect(
    "Select Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

product_range = st.sidebar.slider(
    "Number of Products",
    int(df["NumOfProducts"].min()),
    int(df["NumOfProducts"].max()),
    (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max()))
)

balance_threshold = st.sidebar.slider(
    "Minimum Balance",
    0,
    int(df["Balance"].max()),
    0
)

filtered_df = df[
    (df["Geography"].isin(geography)) &
    (df["Gender"].isin(gender)) &
    (df["NumOfProducts"].between(product_range[0], product_range[1])) &
    (df["Balance"] >= balance_threshold)
]

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🏦 Customer Engagement & Product Utilization Analytics")
st.markdown("### Retention Strategy Dashboard for European Bank Customers")

st.markdown(
    """
This dashboard analyzes customer churn through **engagement behavior, product usage, financial value, 
and relationship strength** to support customer retention strategy.
"""
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
total_customers = len(filtered_df)
churned_customers = filtered_df["Exited"].sum()
retained_customers = total_customers - churned_customers
churn_rate = round((churned_customers / total_customers) * 100, 2) if total_customers > 0 else 0
retention_rate = round(100 - churn_rate, 2)

high_value_disengaged = filtered_df[
    (filtered_df["Balance"] > 100000) &
    (filtered_df["IsActiveMember"] == 0)
]

avg_relationship_score = round(filtered_df["Relationship_Strength_Index"].mean(), 2) if total_customers > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", int(churned_customers))
col3.metric("Churn Rate", f"{churn_rate}%")
col4.metric("Retention Rate", f"{retention_rate}%")
col5.metric("Avg Relationship Score", avg_relationship_score)

st.divider()

# --------------------------------------------------
# Churn Overview
# --------------------------------------------------
st.header("📊 Churn Overview")

c1, c2 = st.columns(2)

with c1:
    churn_count = filtered_df["Exited"].value_counts().reset_index()
    churn_count.columns = ["Exited", "Count"]
    churn_count["Status"] = churn_count["Exited"].map({0: "Retained", 1: "Churned"})

    fig = px.pie(
        churn_count,
        values="Count",
        names="Status",
        title="Customer Churn Distribution",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    geo_churn = filtered_df.groupby("Geography")["Exited"].mean().reset_index()
    geo_churn["Churn Rate (%)"] = geo_churn["Exited"] * 100

    fig = px.bar(
        geo_churn,
        x="Geography",
        y="Churn Rate (%)",
        title="Churn Rate by Geography",
        text="Churn Rate (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Engagement Analysis
# --------------------------------------------------
st.header("🧑‍💼 Engagement vs Churn Analysis")

engagement_churn = filtered_df.groupby("IsActiveMember")["Exited"].mean().reset_index()
engagement_churn["Customer Type"] = engagement_churn["IsActiveMember"].map({
    0: "Inactive Customer",
    1: "Active Customer"
})
engagement_churn["Churn Rate (%)"] = engagement_churn["Exited"] * 100

fig = px.bar(
    engagement_churn,
    x="Customer Type",
    y="Churn Rate (%)",
    title="Active vs Inactive Customer Churn Rate",
    text="Churn Rate (%)"
)
st.plotly_chart(fig, use_container_width=True)

st.info(
    "Business Insight: Inactive customers usually show higher churn risk. "
    "Banks should design engagement campaigns for inactive and low-product customers."
)

# --------------------------------------------------
# Product Utilization Analysis
# --------------------------------------------------
st.header("📦 Product Utilization Impact")

product_churn = filtered_df.groupby("NumOfProducts")["Exited"].mean().reset_index()
product_churn["Churn Rate (%)"] = product_churn["Exited"] * 100

fig = px.bar(
    product_churn,
    x="NumOfProducts",
    y="Churn Rate (%)",
    title="Churn Rate by Number of Products",
    text="Churn Rate (%)"
)
st.plotly_chart(fig, use_container_width=True)

st.success(
    "Product Insight: Product depth is important. Customers using more suitable products "
    "can show stronger relationship value, but poor product fit may increase churn risk."
)

# --------------------------------------------------
# Engagement Profile Analysis
# --------------------------------------------------
st.header("🎯 Engagement Profile Segmentation")

profile_churn = filtered_df.groupby("Engagement_Profile")["Exited"].mean().reset_index()
profile_churn["Churn Rate (%)"] = profile_churn["Exited"] * 100

fig = px.bar(
    profile_churn,
    x="Engagement_Profile",
    y="Churn Rate (%)",
    title="Churn Rate by Engagement Profile",
    text="Churn Rate (%)"
)
fig.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# High Value Disengaged Customer Detector
# --------------------------------------------------
st.header("🚨 High-Value Disengaged Customer Detector")

st.markdown(
    """
These customers have **high account balance** but are **inactive**.  
They are important because they may silently churn even though they look financially valuable.
"""
)

st.metric("High-Value Disengaged Customers", len(high_value_disengaged))

st.dataframe(
    high_value_disengaged[
        [
            "CustomerId",
            "Surname",
            "Geography",
            "Gender",
            "Age",
            "Balance",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "EstimatedSalary",
            "Exited"
        ]
    ].head(50),
    use_container_width=True
)

# --------------------------------------------------
# Relationship Strength Analysis
# --------------------------------------------------
st.header("💪 Relationship Strength Index")

relationship_churn = filtered_df.groupby("Relationship_Category")["Exited"].mean().reset_index()
relationship_churn["Churn Rate (%)"] = relationship_churn["Exited"] * 100

fig = px.bar(
    relationship_churn,
    x="Relationship_Category",
    y="Churn Rate (%)",
    title="Churn Rate by Relationship Strength",
    text="Churn Rate (%)"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**Relationship Strength Index** is calculated using:
- Active membership
- Number of products
- Credit card ownership
- Tenure
"""
)

# --------------------------------------------------
# Credit Card Stickiness
# --------------------------------------------------
st.header("💳 Credit Card Stickiness Score")

card_churn = filtered_df.groupby("HasCrCard")["Exited"].mean().reset_index()
card_churn["Credit Card Status"] = card_churn["HasCrCard"].map({
    0: "No Credit Card",
    1: "Has Credit Card"
})
card_churn["Churn Rate (%)"] = card_churn["Exited"] * 100

fig = px.bar(
    card_churn,
    x="Credit Card Status",
    y="Churn Rate (%)",
    title="Credit Card Ownership vs Churn",
    text="Churn Rate (%)"
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Business Recommendations
# --------------------------------------------------
st.header("✅ Retention Strategy Recommendations")

st.markdown(
    """
### Recommended Actions

1. **Target inactive customers**
   - Send personalized reactivation offers.
   - Provide loyalty rewards for renewed activity.

2. **Improve product bundling**
   - Identify single-product customers and recommend relevant second products.
   - Avoid unnecessary product pushing for unsuitable customers.

3. **Protect high-value disengaged customers**
   - Assign relationship managers to premium inactive customers.
   - Offer exclusive financial advisory or premium banking benefits.

4. **Strengthen credit card engagement**
   - Promote usage-based cashback and reward programs.

5. **Monitor weak relationship customers**
   - Customers with low relationship strength need early retention intervention.
"""
)

# --------------------------------------------------
# Raw Data Preview
# --------------------------------------------------
with st.expander("View Filtered Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)