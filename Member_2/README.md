# 📊 RARITONE – AI Demand Intelligence System

## 📌 Project Overview

RARITONE is an AI-powered demand forecasting system built using Facebook Prophet to analyze **RARITONE’s official dataset (CSV-based)** and generate intelligent business insights.

It is designed for real-world integration with the RARITONE backend dataset to support:

- 📈 Demand Forecasting
- 📦 Inventory Optimization
- 📊 Trend & Seasonality Analysis

---

# 🧠 What I Built

This system consists of **3 independent forecasting modules**, each working on the same RARITONE dataset but producing different business insights.

---

# 📁 Dataset Information (IMPORTANT)

## ⚠️ Official Dataset Used

All modules use:

👉 **RARITONE Dataset (CSV file provided by backend system)**

### Required Dataset Structure:

- A valid **Date column** (Order Date or equivalent)
- A valid **numeric column** (Sales or Quantity)
- Cleaned and preprocessed data (no null values)

---

## 🧹 Dataset Rule

Before processing:

- Date must be converted using `pd.to_datetime()`
- Numeric column must be converted using `pd.to_numeric()`
- Missing values must be removed

---

# 📦 1. inventoryForecast.py

## 🎯 Purpose
Product-level demand forecasting + inventory optimization using RARITONE dataset.

## 💡 What it does
- Filters product-level data from RARITONE dataset
- Aggregates time-series demand
- Applies Prophet forecasting model
- Generates:
  - Future demand prediction
  - Inventory requirement
  - Reorder quantity
  - Growth trend analysis

## 📊 Output
- 6-month product demand forecast
- Inventory recommendation system
- Market trend classification
- Visualization dashboard

---

# 📊 2. productDemand.py

## 🎯 Purpose
Forecasts **overall demand using RARITONE dataset (no filtering)**.

## 💡 What it does
- Uses complete RARITONE dataset
- Aggregates total sales over time
- Applies Prophet forecasting
- Predicts next 6 months demand

## 📊 Output
- Demand forecast report
- Expected / min / max demand
- Trend visualization graph

---

# 📈 3. trendForecasting.py

## 🎯 Purpose
Analyzes **demand trends and seasonality patterns from RARITONE dataset**.

## 💡 What it does
- Uses same RARITONE dataset as productDemand module
- Focuses on:
  - Long-term trend direction
  - Seasonal variations
  - Demand behavior over time
- Generates advanced visualization insights

## 📊 Output
- Trend analysis graph
- Seasonality insights
- Demand behavior interpretation

---

# 📌 Key System Features

✔ Works on RARITONE official dataset  
✔ Modular architecture (3 independent ML pipelines)  
✔ Time-series forecasting using Prophet  
✔ Inventory optimization logic  
✔ Business insight generation  
✔ Trend and seasonality analysis  

---

# 📁 Dataset Dependency

All modules depend on:

👉 **RARITONE CSV Dataset (provided by backend team)**

### Required fields:
- Date column (Order Date or equivalent)
- Numeric column (Sales or Quantity)

---

# 🚀 Business Value

This system enables RARITONE to:

- Predict future product demand
- Optimize inventory levels
- Reduce overstocking & shortages
- Understand seasonal demand patterns
- Improve business decision-making using AI

---

# 📌 Conclusion

This project is fully integrated with the **RARITONE dataset pipeline** and is designed for real-world backend deployment where dataset structure may vary but logic remains stable and modular.

---