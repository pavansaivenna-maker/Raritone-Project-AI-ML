import io
import os
import math
from enum import Enum
import pandas as pd
from prophet import Prophet
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from fastapi import FastAPI, Query, HTTPException, Response
from pydantic import BaseModel
from typing import List

# -------------------------------------------------------------------------
# NATIVE FASHION CATEGORY ENUM SELECTION
# -------------------------------------------------------------------------
class FashionCategory(str, Enum):
    KURTIS = "Kurtis"
    SAREES = "Sarees"
    JEANS = "Jeans"
    SHIRTS = "Shirts"
    TSHIRTS = "T-Shirts"
    HOODIES = "Hoodies"
    JACKETS = "Jackets"
    DRESSES = "Dresses"
    ETHNIC_WEAR = "Ethnic Wear"
    FOOTWEAR = "Footwear"

# -------------------------------------------------------------------------
# PYDANTIC SCHEMAS (Matches Swagger UI Expectations Perfectly)
# -------------------------------------------------------------------------
class CategoryOverview(BaseModel):
    category_analyzed: str
    latest_recorded_demand: float
    projected_next_period_demand: int
    expected_growth_percentage: float
    market_trend: str

class InventoryHealth(BaseModel):
    live_warehouse_stock: int
    recommended_stock_level: int
    safety_buffer: int
    suggested_replenishment: int
    inventory_status: str

class DemandOutlookRow(BaseModel):
    date: str
    projected_demand: float
    minimum_expected_demand: float
    maximum_expected_demand: float

class AnalyticsResponse(BaseModel):
    category_performance: CategoryOverview
    ai_tryon_business_insight: str
    inventory_health: InventoryHealth
    predictive_demand_outlook: List[DemandOutlookRow]

# -------------------------------------------------------------------------
# FASTAPI APP INITIALIZATION
# -------------------------------------------------------------------------
app = FastAPI(
    title="Raritone AI Fashion Intelligence Platform",
    description="Optimized Retail Analytics Engine with Non-Negative Safety Bounds and Low-Volume Smoothing.",
    version="2.5.0"
)

# -------------------------------------------------------------------------
# RELATIONAL DATA EXTRACTION PIPELINE
# -------------------------------------------------------------------------
def get_clean_category_dataframe(category_name: str):
    """Loads CSV files dynamically from Member_2/datasets/ relative to app.py location."""
    CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    order_path = os.path.join(CURRENT_SCRIPT_DIR, "datasets", "order.csv")
    product_path = os.path.join(CURRENT_SCRIPT_DIR, "datasets", "product.csv")
    category_path = os.path.join(CURRENT_SCRIPT_DIR, "datasets", "category.csv")
    
    for f in [order_path, product_path, category_path]:
        if not os.path.exists(f):
            raise HTTPException(
                status_code=500, 
                detail=f"Configuration breakdown. Missing dataset file at: '{f}'"
            )
            
    orders = pd.read_csv(order_path)
    products = pd.read_csv(product_path)
    categories = pd.read_csv(category_path)

    orders = orders.rename(columns={"created_at": "order_date", "status": "order_status"})
    products = products.rename(columns={"id": "product_id", "name": "product_name", "status": "product_status"})
    categories = categories.rename(columns={"id": "category_id", "name": "category_name", "status": "category_status"})

    merged = orders.merge(products, on="product_id", how="inner")
    final_df = merged.merge(categories, on="category_id", how="inner")
    final_df["order_date"] = pd.to_datetime(final_df["order_date"], dayfirst=True, errors="coerce")
    
    segment_df = final_df[final_df["category_name"].str.lower() == category_name.lower()].dropna(subset=["order_date", "quantity"])
    
    # Text-fallback parsing routine for mismatched dataset IDs
    if segment_df.empty:
        singular_keyword = category_name[:-1] if category_name.endswith('s') else category_name
        fallback_df = orders.merge(products, on="product_id", how="inner")
        fallback_df["order_date"] = pd.to_datetime(fallback_df["order_date"], dayfirst=True, errors="coerce")
        
        segment_df = fallback_df[
            fallback_df["product_name"].str.lower().str.contains(singular_keyword.lower(), na=False)
        ].dropna(subset=["order_date", "quantity"])
        
        segment_df["category_name"] = category_name
        live_stock = int(products[products["product_name"].str.lower().str.contains(singular_keyword.lower(), na=False)]["stock"].sum())
    else:
        target_cat_id = segment_df["category_id"].iloc[0]
        live_stock = int(products[products["category_id"] == target_cat_id]["stock"].sum())
        
    if segment_df.empty or len(segment_df) < 2:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category_name}' has insufficient data timeline history to build analytics models."
        )
        
    return segment_df, products, live_stock

def run_fashion_forecasting_engine(category_name: str):
    """Fits the Prophet model on daily grouped transaction counts with non-negative constraints."""
    segment_df, raw_products, live_stock = get_clean_category_dataframe(category_name)

    daily_timeline = segment_df.groupby(pd.Grouper(key="order_date", freq="D"))["quantity"].sum().reset_index().fillna(0)
    forecast_ready = daily_timeline.rename(columns={"order_date": "ds", "quantity": "y"})
    
    # Establish the mathematical baseline floor at 0
    forecast_ready['floor'] = 0
    
    model = Prophet(
        growth='linear',
        yearly_seasonality=False, 
        weekly_seasonality=True, 
        daily_seasonality=False, 
        changepoint_prior_scale=0.05
    )
    model.fit(forecast_ready)

    future = model.make_future_dataframe(periods=14, freq="D")
    future['floor'] = 0 # Carry floor constraints over to look-ahead frames
    
    forecast = model.predict(future)

    # Hard clip negative predictions to 0
    for col in ['yhat', 'yhat_lower', 'yhat_upper']:
        forecast[col] = forecast[col].clip(lower=0)

    return daily_timeline, forecast, model, live_stock

# -------------------------------------------------------------------------
# ROUTE ENDPOINTS
# -------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root_redirect():
    return Response(status_code=307, headers={"Location": "/docs"})

@app.get("/api/v1/raritone/analytics/forecast", response_model=AnalyticsResponse, tags=["Fashion Intelligence Data JSON"])
def get_fashion_demand_forecast(category: FashionCategory = Query(default=FashionCategory.KURTIS)):
    """Returns clean analytical numbers with advanced business rounding logic for micro-demand segments."""
    historical_df, forecast, model, live_stock = run_fashion_forecasting_engine(category.value)
    future_horizon = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(14)

    # 🌟 BUSINESS FIX 1: If fractional user interest exists (> 0), round UP to 1 unit instead of truncating to 0
    raw_next_demand = future_horizon.iloc[0]["yhat"]
    projected_next_period_demand = math.ceil(raw_next_demand) if raw_next_demand > 0 else 0

    # Supply Chain Allocation Matrix
    safety_buffer = 15
    ideal_stock_allocation = projected_next_period_demand + safety_buffer
    replenishment_units_needed = max(0, ideal_stock_allocation - live_stock)

    last_recorded_actual = historical_df["quantity"].iloc[-1] if not historical_df.empty else 0
    
    # 🌟 BUSINESS FIX 2: Refined growth tracking prevents misleading -100% metrics on low volumes
    if last_recorded_actual == 0:
        growth_rate = 0.0
    else:
        growth_rate = round(((projected_next_period_demand - last_recorded_actual) / last_recorded_actual) * 100, 1)

    # Set smart context statuses based on actual target changes
    if growth_rate > 0:
        trend_status = "Accelerating Demand Velocity"
    elif growth_rate < 0:
        trend_status = "Decelerating Demand Volatility"
    else:
        trend_status = "Stabilized / Plateaued Market"

    insight = f"Virtual Try-On user interactions for {category.value} display stable conversion intent."
    stock_status = "Trigger Production Replenishment Run" if replenishment_units_needed > 0 else "Warehouse Levels Healthy"

    future_display = future_horizon.copy()
    future_display["ds"] = future_display["ds"].dt.strftime('%Y-%m-%d')
    
    # Ensure all listed arrays carry perfectly cleaned non-negative boundaries
    outlook_list = [
        DemandOutlookRow(
            date=row["ds"], 
            projected_demand=round(max(0.0, row["yhat"]), 2),
            minimum_expected_demand=round(max(0.0, row["yhat_lower"]), 2), 
            maximum_expected_demand=round(max(0.0, row["yhat_upper"]), 2)
        ) for _, row in future_display.iterrows()
    ]

    return AnalyticsResponse(
        category_performance=CategoryOverview(
            category_analyzed=category.value, 
            latest_recorded_demand=float(last_recorded_actual),
            projected_next_period_demand=int(projected_next_period_demand), 
            expected_growth_percentage=growth_rate, 
            market_trend=trend_status
        ),
        ai_tryon_business_insight=insight,
        inventory_health=InventoryHealth(
            live_warehouse_stock=live_stock, 
            recommended_stock_level=ideal_stock_allocation,
            safety_buffer=safety_buffer, 
            suggested_replenishment=replenishment_units_needed, 
            inventory_status=stock_status
        ),
        predictive_demand_outlook=outlook_list
    )

@app.get("/api/v1/raritone/visual/dashboard", tags=["Visualizations (Renders Direct Images)"])
def get_dashboard_chart_rendered(category: FashionCategory = Query(default=FashionCategory.KURTIS)):
    """Generates and serves the prediction chart directly to your browser as a clean PNG image."""
    historical_df, forecast, _, _ = run_fashion_forecasting_engine(category.value)
    
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(historical_df["order_date"], historical_df["quantity"], linewidth=3, label="Actual Purchases", color="#e83e8c")
    ax.plot(forecast["ds"], forecast["yhat"], linewidth=3, label="AI Predictive Target", color="#6f42c1")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], alpha=0.15, color="#6f42c1")
    ax.axvline(historical_df["order_date"].max(), linestyle="--", linewidth=2, color="#28a745")
    ax.set_title(f"RARITONE DEMAND PREDICTION DASHBOARD: {category.value.upper()}", fontweight="bold")
    ax.set_xlabel("Date Timeline")
    ax.set_ylabel("Quantity Ordered")
    ax.set_ylim(bottom=0) # Keeps chart plots from clipping underneath zero
    ax.legend(loc="upper left")
    plt.tight_layout()
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close(fig)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/api/v1/raritone/visual/drivers", tags=["Visualizations (Renders Direct Images)"])
def get_drivers_chart_rendered(category: FashionCategory = Query(default=FashionCategory.KURTIS)):
    """Generates and serves the weekly trend components directly to your browser as a clean PNG image."""
    _, forecast, model, _ = run_fashion_forecasting_engine(category.value)
    fig2 = model.plot_components(forecast)
    plt.tight_layout()
    
    buf = io.BytesIO()
    fig2.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close(fig2)
    return Response(content=buf.getvalue(), media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("inventoryForecast:app", host="127.0.0.1", port=8000, reload=True)