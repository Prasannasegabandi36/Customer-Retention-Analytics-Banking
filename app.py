import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Banking Retention Intelligence",
    page_icon="🏦",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #061627 0%, #0B2D4D 50%, #003B73 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020B14, #061627, #0B2D4D);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.block-container {
    padding-top: 2rem;
}

.big-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    padding-top: 10px;
}

.sub-title {
    font-size: 18px;
    color: #D7E9FF;
    margin-bottom: 25px;
}

.kpi-card {
    background: linear-gradient(135deg, #005B96, #00A6FB);
    padding: 24px;
    border-radius: 22px;
    color: white;
    text-align: center;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.25);
}

.kpi-value {
    font-size: 32px;
    font-weight: 900;
}

.kpi-label {
    font-size: 14px;
    color: #E8F4FF;
}

.insight-box {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-left: 7px solid #00A6FB;
    border-radius: 14px;
    font-size: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.20);
    color: #0B1F3A;
}

.warning-box {
    background: rgba(255,244,229,0.98);
    padding: 20px;
    border-left: 7px solid #FFB703;
    border-radius: 14px;
    font-size: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.20);
    color: #0B1F3A;
}

.success-box {
    background: rgba(232,255,241,0.98);
    padding: 20px;
    border-left: 7px solid #00A86B;
    border-radius: 14px;
    font-size: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.20);
    color: #0B1F3A;
}

h1, h2, h3 {
    color: white !important;
    font-weight: 800;
}

p, label, span {
    color: inherit;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.18);
    border-radius: 14px;
    padding: 12px 18px;
    font-weight: 700;
    color: white;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00A6FB, #0074D9);
    color: white;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.15);
    padding: 18px;
    border-radius: 18px;
    color: white;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
}

[data-testid="stDataFrame"] {
    background: white;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("European_Bank.csv")

df = load_data()

# ---------------- FEATURE ENGINEERING ----------------
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

df["Retention_Intelligence_Score"] = (
    df["Relationship_Strength_Index"] * 20 +
    df["IsActiveMember"] * 20 +
    np.where(df["Balance"] > 100000, 10, 0)
)

# Safer than np.select for Streamlit Cloud / NumPy compatibility
df["Risk_Level"] = "High Risk"
df.loc[df["Retention_Intelligence_Score"] >= 80, "Risk_Level"] = "Low Risk"
df.loc[
    (df["Retention_Intelligence_Score"] >= 50) &
    (df["Retention_Intelligence_Score"] < 80),
    "Risk_Level"
] = "Medium Risk"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏦 Control Panel")
st.sidebar.markdown("Use filters to explore banking retention behavior.")

geography = st.sidebar.multiselect(
    "🌍 Select Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender = st.sidebar.multiselect(
    "👤 Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

active_status = st.sidebar.multiselect(
    "⚡ Active Status",
    df["IsActiveMember"].unique(),
    default=df["IsActiveMember"].unique()
)

product_range = st.sidebar.slider(
    "📦 Number of Products",
    int(df["NumOfProducts"].min()),
    int(df["NumOfProducts"].max()),
    (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max()))
)

balance_threshold = st.sidebar.slider(
    "💰 Minimum Balance",
    0,
    int(df["Balance"].max()),
    0
)

filtered_df = df[
    (df["Geography"].isin(geography)) &
    (df["Gender"].isin(gender)) &
    (df["IsActiveMember"].isin(active_status)) &
    (df["NumOfProducts"].between(product_range[0], product_range[1])) &
    (df["Balance"] >= balance_threshold)
]

# ---------------- HEADER ----------------
st.markdown(
    '<div class="big-title">🏦 Customer Retention Intelligence Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">💼 Banking Analytics • 📊 Churn Intelligence • 🧠 Customer Segmentation • 🚀 Retention Strategy</div>',
    unsafe_allow_html=True
)

st.write("")

# ---------------- KPI CALCULATIONS ----------------
total_customers = len(filtered_df)
churned = int(filtered_df["Exited"].sum()) if total_customers > 0 else 0
retained = total_customers - churned
churn_rate = round((churned / total_customers) * 100, 2) if total_customers > 0 else 0
retention_rate = round(100 - churn_rate, 2)
avg_score = round(filtered_df["Retention_Intelligence_Score"].mean(), 2) if total_customers > 0 else 0

high_value_risk = filtered_df[
    (filtered_df["Balance"] > 100000) &
    (filtered_df["IsActiveMember"] == 0)
]

# ---------------- KPI CARDS ----------------
c1, c2, c3, c4, c5 = st.columns(5)

for col, label, value in [
    (c1, "👥 Total Customers", f"{total_customers:,}"),
    (c2, "📉 Churn Rate", f"{churn_rate}%"),
    (c3, "✅ Retained Customers", f"{retained:,}"),
    (c4, "⚠️ Churned Customers", f"{churned:,}"),
    (c5, "🧠 Avg Retention Score", avg_score)
]:
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Command Center",
    "🧠 Customer Intelligence",
    "🚨 Premium Risk Radar",
    "💎 Relationship Strength",
    "🎯 Strategy Playbook"
])

# ---------------- TAB 1 ----------------
with tab1:
    st.header("📊 Executive Retention Overview")

    col1, col2 = st.columns(2)

    with col1:
        churn_df = filtered_df["Exited"].value_counts().reset_index()
        churn_df.columns = ["Exited", "Count"]
        churn_df["Status"] = churn_df["Exited"].map({0: "Retained", 1: "Churned"})

        fig = px.pie(
            churn_df,
            values="Count",
            names="Status",
            hole=0.55,
            title="Customer Churn Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        geo_churn = filtered_df.groupby("Geography")["Exited"].mean().reset_index()
        geo_churn["Churn Rate (%)"] = (geo_churn["Exited"] * 100).round(2)

        fig = px.bar(
            geo_churn,
            x="Geography",
            y="Churn Rate (%)",
            text="Churn Rate (%)",
            title="Geography-wise Churn Rate"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="insight-box">
        📌 <b>Strategic Insight:</b> Churn is not only a customer loss metric. 
        It represents weak engagement, low relationship depth, and missed retention opportunities.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- TAB 2 ----------------
with tab2:
    st.header("🧠 Customer Engagement & Product Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        engagement = filtered_df.groupby("IsActiveMember")["Exited"].mean().reset_index()
        engagement["Customer Type"] = engagement["IsActiveMember"].map({
            0: "Inactive Customer",
            1: "Active Customer"
        })
        engagement["Churn Rate (%)"] = (engagement["Exited"] * 100).round(2)

        fig = px.bar(
            engagement,
            x="Customer Type",
            y="Churn Rate (%)",
            text="Churn Rate (%)",
            title="Active vs Inactive Churn"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        product = filtered_df.groupby("NumOfProducts")["Exited"].mean().reset_index()
        product["Churn Rate (%)"] = (product["Exited"] * 100).round(2)

        fig = px.bar(
            product,
            x="NumOfProducts",
            y="Churn Rate (%)",
            text="Churn Rate (%)",
            title="Product Utilization vs Churn"
        )
        st.plotly_chart(fig, use_container_width=True)

    profile = filtered_df.groupby("Engagement_Profile")["Exited"].mean().reset_index()
    profile["Churn Rate (%)"] = (profile["Exited"] * 100).round(2)

    fig = px.bar(
        profile,
        x="Engagement_Profile",
        y="Churn Rate (%)",
        text="Churn Rate (%)",
        title="Engagement Profile Churn Intelligence"
    )
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="success-box">
        ✅ <b>Business Meaning:</b> Active and multi-product customers usually show stronger retention. 
        Inactive low-product users need immediate retention campaigns.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- TAB 3 ----------------
with tab3:
    st.header("🚨 Premium Customer Risk Radar")

    st.markdown(
        """
        <div class="warning-box">
        ⚠️ <b>Premium Risk Logic:</b> Customers with balance above 100,000 and inactive status 
        are classified as high-value disengaged customers.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric("💰 High-Value Disengaged Customers", len(high_value_risk))

    if len(high_value_risk) > 0:
        risk_geo = high_value_risk.groupby("Geography")["CustomerId"].count().reset_index()
        risk_geo.columns = ["Geography", "Risk Customers"]

        fig = px.bar(
            risk_geo,
            x="Geography",
            y="Risk Customers",
            text="Risk Customers",
            title="Premium Risk Customers by Geography"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            high_value_risk[
                [
                    "CustomerId", "Surname", "Geography", "Gender",
                    "Age", "Balance", "NumOfProducts",
                    "IsActiveMember", "EstimatedSalary", "Exited"
                ]
            ].head(50),
            use_container_width=True
        )
    else:
        st.success("No premium risk customers found for selected filters.")

# ---------------- TAB 4 ----------------
with tab4:
    st.header("💎 Relationship Strength & Retention Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        rel = filtered_df.groupby("Relationship_Category")["Exited"].mean().reset_index()
        rel["Churn Rate (%)"] = (rel["Exited"] * 100).round(2)

        fig = px.bar(
            rel,
            x="Relationship_Category",
            y="Churn Rate (%)",
            text="Churn Rate (%)",
            title="Relationship Strength vs Churn"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        risk = filtered_df["Risk_Level"].value_counts().reset_index()
        risk.columns = ["Risk Level", "Customers"]

        fig = px.pie(
            risk,
            values="Customers",
            names="Risk Level",
            hole=0.45,
            title="Retention Risk Segmentation"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📌 Customer Segment Summary")

    segment_summary = filtered_df.groupby("Risk_Level").agg(
        Customers=("CustomerId", "count"),
        Avg_Balance=("Balance", "mean"),
        Avg_Retention_Score=("Retention_Intelligence_Score", "mean"),
        Churn_Rate=("Exited", "mean")
    ).reset_index()

    segment_summary["Avg_Balance"] = segment_summary["Avg_Balance"].round(2)
    segment_summary["Avg_Retention_Score"] = segment_summary["Avg_Retention_Score"].round(2)
    segment_summary["Churn_Rate"] = (segment_summary["Churn_Rate"] * 100).round(2)

    st.dataframe(segment_summary, use_container_width=True)

# ---------------- TAB 5 ----------------
with tab5:
    st.header("🎯 Strategic Retention Playbook")

    st.markdown(
        """
        ### 1. 🔄 Customer Reactivation Strategy
        Target inactive customers with personalized reactivation campaigns, relationship manager calls, and reward-based engagement offers.

        ### 2. 📦 Product Bundling Optimization
        Identify single-product customers and recommend suitable second products such as credit cards, savings plans, or advisory services.

        ### 3. 💰 Premium Customer Protection
        High-balance inactive customers should be treated as silent churn risks and monitored through proactive retention programs.

        ### 4. 🧠 Relationship Intelligence System
        Use the Relationship Strength Index to classify customers into weak, medium, and strong relationship groups.

        ### 5. 🚨 Churn Prevention Dashboard
        The dashboard can support early-warning systems for customer loyalty teams and banking CRM departments.
        """
    )

    st.markdown(
        """
        <div class="insight-box">
        🚀 <b>Final Business Impact:</b> This dashboard converts raw banking data into customer retention intelligence, 
        helping banks identify risk early, improve product adoption, and reduce churn through engagement-driven strategies.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- RAW DATA ----------------
with st.expander("📂 View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
