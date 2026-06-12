# Raritone AI Demand & Financial Intelligence Platform

An enterprise-grade, decentralized network of machine learning microservices engineered to provide predictive retail analytics. Utilizing **FastAPI** for high-performance API routing and **Facebook Prophet** for time-series forecasting, this platform transforms raw historical transaction logs into actionable inventory buffers, automated manufacturing replenishment flags, and 6-month macro revenue trajectories.

---

##  1. Data Architecture & Relational Schema

The forecasting pipeline aggregates data from three foundational relational structures located within the local `/datasets` directory. The engines automatically execute internal relational joins (`inner merges`) using shared primary keys to map transactions to their specific apparel category profiles.

### Directory Blueprint  


Member_2/
├── datasets/
│   ├── order.csv                # Core Transaction Ledger
│   ├── product.csv              # Product Catalog & Live Stock Index
│   └── category.csv             # Operational Taxonomy Hierarchy
├── inventoryForecast.py         # App 1: Daily Units Operations (Port 8000)
├── productDemand.py             # App 2: 6-Month Units Projection (Port 8001)
├── trendForecasting.py          # App 3: 6-Month Financial Trajectory (Port 8002)
├── requirements.txt             # Consolidated system dependencies


## Relational Entity Layout

[order.csv]                    [product.csv]                  [category.csv]
+---------------+              +---------------+              +---------------+
| id            |              | id            |              | id            |
| product_id    | <----------> | name          |              | name          |
| quantity      |              | price         |              | status        |
| status        |              | stock         | <----------> |               |
| created_at    |              | category_id   |              |               |
+---------------+              +---------------+              +---------------+


## The Three Predictive AI Engines

To optimize performance and isolate runtime parameters, the platform splits its features into three standalone Python microservices. They run completely independently on separate network ports.

### 🔹 App 1: Daily Operations Forecasting (inventoryForecast.py)
Core Focus: Short-Term Micro-Fulfillment & Warehouse Inventory Health.

Network Port: 8000

Timeline Interval: Daily (D frequency granularity)

Description: Monitors immediate transactional patterns to predict sales over an upcoming 14-day window. It aggregates daily sales, clips negative bounds to 0, compares projected requirements against active warehouse stock, and outputs an automated supply chain alert (Warehouse Levels Healthy or Trigger Production Replenishment Run).

### 🔹 App 2: 6-Month Product Demand Strategic Engine (productDemand.py)
Core Focus: Mid-to-Long Range Manufacturing Run Allocation.

Network Port: 8001

Timeline Interval: Month-End (ME frequency granularity)

Description: Built for production planners. It analyzes macro-level demand signals by grouping units over long monthly buckets. This smooths out short-term noise to project volume requirements across a 6-month outlook horizon.

### 🔹 App 3: 6-Month Financial & Revenue Trajectory Engine (trendForecasting.py)
Core Focus: Gross Revenue, Financial Planning, and Budget Forecasting.

Network Port: 8002

Timeline Interval: Month-End (ME frequency granularity)

Description: Swaps volume tracking for currency tracking. It multiplies order quantities by individual unit costs to map historical revenue trends. It generates a 6-month forecast of incoming revenue stream values (in ₹ Rupees), paired with a breakdown of annual sales seasonality patterns.

# DO READ DEPLOYMENT DETAILS AND REQUIREMENTS
