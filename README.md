# 🏦 Customer Retention Analytics Banking

### Customer Engagement & Product Utilization Analytics for Retention Strategy

🔗 **Live Dashboard:**  
https://customer-retention-analytics-banking-nksykt8w2y2v2vzqqcfoc4.streamlit.app/

---

## 📌 Project Overview

This project analyzes customer churn in a European bank by focusing on **customer engagement, product usage, financial value, and relationship strength**.

Instead of only asking *“Who will churn?”*, this project answers:

> **Why are customers leaving, and how can the bank retain them?**

---

## 🎯 Business Problem

Banks may lose customers even when they have:

- High account balance
- Good credit score
- Long tenure
- High estimated salary

This happens when customers are:

- Inactive
- Using fewer banking products
- Weakly connected with the bank
- Not engaged with banking services

---

## 🧠 Project Objective

The goal is to identify:

- High-risk churn customers
- Inactive premium customers
- Product usage impact on churn
- Strong vs weak customer relationships
- Retention opportunities for the bank

---

## 🛠️ Tools & Technologies

- **Python** – Data analysis and feature engineering
- **Pandas / NumPy** – Data processing
- **Plotly** – Interactive visualizations
- **Streamlit** – Web dashboard
- **Google Colab** – EDA and ML experimentation
- **GitHub** – Project version control

---

## 📊 Dataset

The dataset contains **10,000 European bank customers**.

Key columns include:

- CustomerId
- CreditScore
- Geography
- Gender
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard
- IsActiveMember
- EstimatedSalary
- Exited

`Exited` is the target column:

- `0` = Retained customer
- `1` = Churned customer

---

## 📈 Key KPIs

| KPI | Purpose |
|---|---|
| Churn Rate | Measures customer loss |
| Retention Rate | Measures customer loyalty |
| Engagement Retention Ratio | Compares active vs inactive retention |
| Product Depth Index | Measures product adoption |
| High-Balance Disengagement Rate | Finds premium customers at risk |
| Credit Card Stickiness Score | Measures card ownership retention impact |
| Relationship Strength Index | Scores customer relationship depth |

---

## 🚀 Dashboard Features

The Streamlit dashboard includes:

- Overall churn overview
- Geography-wise churn analysis
- Active vs inactive customer churn
- Product utilization impact
- Engagement profile segmentation
- High-value disengaged customer detector
- Relationship strength analysis
- Credit card stickiness analysis
- Interactive filters for geography, gender, product count, and balance

---

## 🔍 Customer Segments Created

Customers were classified into engagement profiles:

- Active Engaged Customer
- Active Low-Product Customer
- Inactive Disengaged Customer
- Inactive High-Balance Customer

This helps the bank understand which customers need retention focus.

---

## 💪 Relationship Strength Index

A custom relationship score was created using:

- Active membership
- Number of products
- Credit card ownership
- Tenure

Customers were grouped into:

- Weak Relationship
- Medium Relationship
- Strong Relationship

---

## 💡 Business Insights

- Inactive customers show higher churn risk.
- Product usage strongly affects retention.
- High-balance inactive customers are premium customers at risk.
- Relationship strength is a better loyalty indicator than balance alone.
- Banks should focus on behavioral engagement, not only financial value.

---

## ✅ Retention Recommendations

- Launch reactivation campaigns for inactive customers.
- Offer personalized product bundles.
- Monitor high-balance disengaged customers.
- Improve loyalty rewards for credit card users.
- Use relationship strength scoring for early churn prevention.

---

## 📌 Project Workflow

```text
CSV Dataset
   ↓
Google Colab EDA
   ↓
Feature Engineering
   ↓
Streamlit Dashboard
   ↓
Business Insights
   ↓
Retention Strategy
