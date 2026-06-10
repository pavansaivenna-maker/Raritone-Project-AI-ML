import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 22
plt.rcParams["axes.labelsize"] = 13
plt.rcParams["legend.fontsize"] = 11

sales = pd.read_csv(
    "Sample - Superstore.csv",
    encoding="latin1"
)

sales["Order Date"] = pd.to_datetime(
    sales["Order Date"],
    errors="coerce"
)

sales["Quantity"] = pd.to_numeric(
    sales["Quantity"],
    errors="coerce"
)

sales = sales.dropna(
    subset=[
        "Order Date",
        "Quantity"
    ]
)

product_name = "Oversized T-Shirts"

product_sales = sales[
    sales["Sub-Category"] == "Phones"
]

monthly_demand = (
    product_sales
    .groupby(
        pd.Grouper(
            key="Order Date",
            freq="ME"
        )
    )["Quantity"]
    .sum()
    .reset_index()
)

forecast_data = monthly_demand.rename(
    columns={
        "Order Date": "ds",
        "Quantity": "y"
    }
)

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)

model.fit(forecast_data)

future = model.make_future_dataframe(
    periods=6,
    freq="ME"
)

forecast = model.predict(future)

future_forecast = forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
].tail(6)

current_stock = 150
safety_stock = 30

next_month_demand = max(
    0,
    round(
        future_forecast.iloc[0]["yhat"]
    )
)

required_inventory = (
    next_month_demand
    + safety_stock
)

reorder_quantity = max(
    0,
    required_inventory
    - current_stock
)

last_actual = monthly_demand["Quantity"].iloc[-1]

growth_rate = round(
    (
        (
            next_month_demand
            - last_actual
        )
        / last_actual
    ) * 100,
    1
)

print("\n" + "=" * 80)
print("RARITONE VENDOR ANALYTICS PLATFORM")
print("AI-Powered Demand Intelligence & Inventory Optimization")
print("=" * 80)

print("\nCATEGORY PERFORMANCE OVERVIEW")
print("-" * 80)

print(f"Category Analyzed           : {product_name}")
print(f"Latest Recorded Demand      : {last_actual} Orders")
print(f"Projected Next Month Demand : {next_month_demand} Orders")
print(f"Expected Growth             : {growth_rate}%")

if growth_rate > 0:
    trend_status = "Trending Upward"
else:
    trend_status = "Stable / Declining"

print(f"Market Trend                : {trend_status}")

print("\nAI BUSINESS INSIGHT")
print("-" * 80)

if growth_rate > 0:
    print(
        f"Demand for {product_name} is expected to increase over the coming month. "
        f"Vendors should prepare for higher customer interest and maintain adequate inventory levels."
    )
else:
    print(
        f"Demand for {product_name} is expected to remain stable. "
        f"Current inventory allocation appears sufficient."
    )

print("\nINVENTORY HEALTH")
print("-" * 80)

print(f"Current Inventory           : {current_stock} Units")
print(f"Recommended Inventory Level : {required_inventory} Units")
print(f"Safety Buffer               : {safety_stock} Units")
print(f"Suggested Replenishment     : {reorder_quantity} Units")

if reorder_quantity > 0:
    print("Inventory Status            : Replenishment Recommended")
else:
    print("Inventory Status            : Healthy Inventory Position")

future_display = future_forecast.copy()

future_display.columns = [
    "Month",
    "Projected Demand",
    "Minimum Expected Demand",
    "Maximum Expected Demand"
]

print("\n6-MONTH DEMAND OUTLOOK")
print("-" * 80)
print(future_display)

fig, ax = plt.subplots(
    figsize=(16, 8)
)

ax.plot(
    monthly_demand["Order Date"],
    monthly_demand["Quantity"],
    linewidth=3,
    label="Historical Demand"
)

ax.plot(
    forecast["ds"],
    forecast["yhat"],
    linewidth=3,
    label="AI Demand Projection"
)

ax.fill_between(
    forecast["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.12,
    label="Forecast Range"
)

forecast_start = monthly_demand["Order Date"].max()

ax.axvline(
    forecast_start,
    linestyle="--",
    linewidth=2,
    alpha=0.8,
    label="Forecast Start"
)

ax.set_title(
    "RARITONE DEMAND INTELLIGENCE DASHBOARD",
    fontweight="bold",
    pad=25
)

fig.text(
    0.5,
    0.92,
    "Historical Customer Demand vs AI-Predicted Demand",
    ha="center",
    fontsize=14
)

ax.set_xlabel(
    "Timeline",
    fontsize=13
)

ax.set_ylabel(
    "Customer Orders",
    fontsize=13
)

ax.legend(
    loc="upper left",
    bbox_to_anchor=(0.01, 0.99),
    frameon=True,
    fancybox=True,
    shadow=True,
    fontsize=11
)

ax.text(
    0.98,
    0.82,
    f"Projected Growth\n {growth_rate}%",
    transform=ax.transAxes,
    fontsize=13,
    fontweight="bold",
    ha="right",
    va="top",
    bbox=dict(
        boxstyle="round,pad=0.7",
        facecolor="white",
        edgecolor="gray",
        alpha=0.95
    )
)

ax.grid(
    True,
    alpha=0.3
)

plt.tight_layout(
    rect=[0, 0, 1, 0.93]
)

plt.show()

fig2 = model.plot_components(
    forecast
)

for axis in fig2.axes:
    axis.grid(
        True,
        alpha=0.3
    )

plt.suptitle(
    "RARITONE DEMAND DRIVERS ANALYSIS",
    fontsize=18,
    fontweight="bold"
)

plt.tight_layout()

plt.show()