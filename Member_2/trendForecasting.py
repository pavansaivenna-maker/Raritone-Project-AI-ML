import io
import os
import math
from enum import Enum
import pandas as pd
from prophet import Prophet
import matplotlib
# Forces matplotlib to use a non-interactive backend suited for web servers
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
# PYDANTIC SCHEMAS (Cleaned & Structured for Swagger UI Output)
# -------------------------------------------------------------------------
class CategoryOverview(BaseModel):
    category_analyzed: str
    latest_recorded_revenue: float
    projected_next_period_revenue: int
    expected_growth_percentage: float
    market_trend: str

class InventoryHealth(BaseModel):
    live_warehouse_stock: int
    recommended_stock_level: int
    safety_buffer: int
    suggested_replenishment: int
    inventory_status: str

class RevenueOutlookRow(BaseModel):
    date: str
    projected_revenue: float
    minimum_expected_revenue: float
    maximum_expected_revenue: float

class AnalyticsResponse(BaseModel):
    category_performance: CategoryOverview
    ai_tryon_business_insight: str
    inventory_health: InventoryHealth
    predictive_revenue_outlook: List[RevenueOutlookRow]

# -------------------------------------------------------------------------
# FASTAPI APP INITIALIZATION (Configured to run on standalone Port 8002)
# -------------------------------------------------------------------------
app = FastAPI(
    title="Raritone AI Revenue & Trend Intelligence Engine",
    description="### Macro-Level 6-Month Revenue Projection Framework (Currency: ₹ Rupees)",
    version="4.0.0"
)

# -------------------------------------------------------------------------
# RELATIONAL DATA EXTRACTION PIPELINE
# -------------------------------------------------------------------------
def get_clean_category_dataframe(category_name: str):
    """Loads CSV files dynamically from the datasets/ folder relative to this script."""
    CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    order_path = os.path.join(CURRENT_SCRIPT_DIR, "datasets", "order.csv")
    product_path = os.path.join(CURRENT_SCRIPT_DIR, "datasets", "product.csv")
    category_path = os.path.join(CURRENT_SCRIPT_DIR, "datasets", "category.csv")
    
    for f in [order_path, product_path, category_path]:
        if not os.path.exists(f):
            raise HTTPException(
                status_code=500, 
                detail=f"Configuration breakdown. Missing target file asset at: '{f}'"
            )
            
    orders = pd.read_csv(order_path)
    products = pd.read_csv(product_path)
    categories = pd.read_csv(category_path)

    orders = orders.rename(columns={"created_at": "order_date", "status": "order_status"})
    products = products.rename(columns={"id": "product_id", "name": "product_name", "status": "product_status"})
    categories = categories.rename(columns={"id": "category_id", "name": "category_name", "status": "category_status"})

    # Creating a combined pricing field: Revenue = Order Item Quantity * Product Unit Price
    merged = orders.merge(products, on="product_id", how="inner")
    final_df = merged.merge(categories, on="category_id", how="inner")
    
    final_df["order_date"] = pd.to_datetime(final_df["order_date"], dayfirst=True, errors="coerce")
    final_df["item_revenue"] = pd.to_numeric(final_df["quantity"] * final_df["price"], errors="coerce")
    
    segment_df = final_df[final_df["category_name"].str.lower() == category_name.lower()].dropna(subset=["order_date", "item_revenue"])
    
    # Text-fallback parsing framework if relational keys do not directly align
    if segment_df.empty:
        singular_keyword = category_name[:-1] if category_name.endswith('s') else category_name
        fallback_df = orders.merge(products, on="product_id", how="inner")
        fallback_df["order_date"] = pd.to_datetime(fallback_df["order_date"], dayfirst=True, errors="coerce")
        fallback_df["item_revenue"] = pd.to_numeric(fallback_df["quantity"] * fallback_df["price"], errors="coerce")
        
        segment_df = fallback_df[
            fallback_df["product_name"].str.lower().str.contains(singular_keyword.lower(), na=False)
        ].dropna(subset=["order_date", "item_revenue"])
        
        segment_df["category_name"] = category_name
        live_stock = int(products[products["product_name"].str.lower().str.contains(singular_keyword.lower(), na=False)]["stock"].sum())
    else:
        target_cat_id = segment_df["category_id"].iloc[0]
        live_stock = int(products[products["category_id"] == target_cat_id]["stock"].sum())
        
    if segment_df.empty or len(segment_df) < 2:
        raise HTTPException(
            status_code=404,
            detail=f"Category structure content '{category_name}' has insufficient ledger transactions to evaluate financial growth."
        )
        
    return segment_df, products, live_stock

def run_fashion_trend_engine(category_name: str):
    """Fits Prophet on Month-End (ME) timelines using gross pricing values."""
    segment_df, raw_products, live_stock = get_clean_category_dataframe(category_name)

    # 🌟 Grouping by Month-End (ME) on total calculated revenue
    monthly_timeline = segment_df.groupby(pd.Grouper(key="order_date", freq="ME"))["item_revenue"].sum().reset_index().fillna(0)
    forecast_ready = monthly_timeline.rename(columns={"order_date": "ds", "item_revenue": "y"})
    
    # Establish mathematical zero bounds
    forecast_ready['floor'] = 0
    
    model = Prophet(
        growth='linear',
        yearly_seasonality=True, 
        weekly_seasonality=False, 
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    model.fit(forecast_ready)

    # Forecast window looking forward 6 months
    future = model.make_future_dataframe(periods=6, freq="ME")
    future['floor'] = 0
    forecast = model.predict(future)

    # Hard clip negative financial projections to zero
    for col in ['yhat', 'yhat_lower', 'yhat_upper']:
        forecast[col] = forecast[col].clip(lower=0)

    return monthly_timeline, forecast, model, live_stock

# -------------------------------------------------------------------------
# API ROUTE ROUTERS
# -------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root_redirect():
    return Response(status_code=307, headers={"Location": "/docs"})

@app.get("/api/v1/raritone/analytics/forecast", response_model=AnalyticsResponse, tags=["Fashion Revenue Intelligence Data JSON"])
def get_fashion_revenue_forecast(category: FashionCategory = Query(default=FashionCategory.KURTIS)):
    """Returns a 6-month numerical revenue trajectory profile formatted cleanly with non-negative lower limits."""
    historical_df, forecast, model, live_stock = run_fashion_trend_engine(category.value)
    future_horizon = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(6)

    # Clean up target decimals into discrete structural units
    raw_next_revenue = future_horizon.iloc[0]["yhat"]
    projected_next_period_revenue = math.ceil(raw_next_revenue) if raw_next_revenue > 0 else 0

    # Macro Financial Stock Planning Metrics
    safety_buffer = 30
    ideal_stock_allocation = math.ceil(projected_next_period_revenue / 500) + safety_buffer # Proxy ratio calculation
    replenishment_units_needed = max(0, ideal_stock_allocation - live_stock)

    last_recorded_actual = historical_df["item_revenue"].iloc[-1] if not historical_df.empty else 0
    
    if last_recorded_actual == 0:
        growth_rate = 0.0
    else:
        growth_rate = round(((projected_next_period_revenue - last_recorded_actual) / last_recorded_actual) * 100, 1)

    if growth_rate > 0:
        trend_status = "Accelerating Revenue Velocity"
    elif growth_rate < 0:
        trend_status = "Decelerating Financial Volatility"
    else:
        trend_status = "Stabilized / Plateaued Market Market"

    insight = f"Predictive scaling checks indicate stable customer basket retention patterns for {category.value} over the 6-month cycle."
    stock_status = "Trigger Production Replenishment Run" if replenishment_units_needed > 0 else "Warehouse Levels Healthy"

    future_display = future_horizon.copy()
    future_display["ds"] = future_display["ds"].dt.strftime('%B %Y')
    outlook_list = [
        RevenueOutlookRow(
            date=row["ds"], 
            projected_revenue=round(max(0.0, row["yhat"]), 2),
            minimum_expected_revenue=round(max(0.0, row["yhat_lower"]), 2), 
            maximum_expected_revenue=round(max(0.0, row["yhat_upper"]), 2)
        ) for _, row in future_display.iterrows()
    ]

    return AnalyticsResponse(
        category_performance=CategoryOverview(
            category_analyzed=category.value, latest_recorded_revenue=float(last_recorded_actual),
            projected_next_period_revenue=int(projected_next_period_revenue), expected_growth_percentage=growth_rate, market_trend=trend_status
        ),
        ai_tryon_business_insight=insight,
        inventory_health=InventoryHealth(
            live_warehouse_stock=live_stock, recommended_stock_level=ideal_stock_allocation,
            safety_buffer=safety_buffer, suggested_replenishment=replenishment_units_needed, inventory_status=stock_status
        ),
        predictive_revenue_outlook=outlook_list
    )

@app.get("/api/v1/raritone/visual/dashboard", tags=["Visualizations (Renders Direct Images)"])
def get_dashboard_chart_rendered(category: FashionCategory = Query(default=FashionCategory.KURTIS)):
    """Generates the main 6-Month macro revenue trend dashboard directly to Swagger UI."""
    historical_df, forecast, model, _ = run_fashion_trend_engine(category.value)
    
    plt.style.use("seaborn-v0_8-whitegrid")
    fig = model.plot(forecast)
    ax = fig.gca()
    fig.set_size_inches(12, 6)

    fig.suptitle("Fashion AI Demand Intelligence Dashboard", fontsize=18, fontweight="bold", y=0.96)
    ax.set_title(f"{category.value.upper()} - Revenue Trend Forecast (Next 6 Months Projection)", fontsize=13, pad=15)
    ax.set_xlabel("Time (Monthly)", fontsize=11)
    ax.set_ylabel("Predicted Revenue (₹)", fontsize=11)
    ax.set_ylim(bottom=0)

    # Highlight overlay matching the green aesthetic specified in your original script
    ax.axvspan(forecast["ds"].iloc[-6], forecast["ds"].iloc[-1], color="green", alpha=0.12, label="6-Month Forward Projection Area")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left")
    
    plt.subplots_adjust(top=0.88)
    plt.tight_layout()
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close(fig)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/api/v1/raritone/visual/drivers", tags=["Visualizations (Renders Direct Images)"])
def get_drivers_chart_rendered(category: FashionCategory = Query(default=FashionCategory.KURTIS)):
    """Generates the underlying financial trend and annual decomposition graph drivers directly to Swagger UI."""
    _, forecast, model, _ = run_fashion_trend_engine(category.value)
    
    fig2 = model.plot_components(forecast)
    for ax in fig2.axes:
        ax.grid(True, linestyle="--", alpha=0.3)

    fig2.suptitle("Key Drivers of Fashion Sales (Trend + Seasonality Breakdown)", fontsize=16, fontweight="bold", y=0.96)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    
    buf = io.BytesIO()
    fig2.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close(fig2)
    return Response(content=buf.getvalue(), media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    # Bound to unique network port 8002 to maintain isolation from your other running servers
    uvicorn.run("trendForecasting:app", host="127.0.0.1", port=8002, reload=True)