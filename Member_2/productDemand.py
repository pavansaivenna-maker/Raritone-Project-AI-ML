import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

sales = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

print("Raritone AI Demand Intelligence System Activated")
print("Dataset Loaded:", sales.shape)

sales["Order Date"] = pd.to_datetime(sales["Order Date"], errors="coerce")
sales["Sales"] = pd.to_numeric(sales["Sales"], errors="coerce")

sales = sales.dropna(subset=["Order Date", "Sales"])

monthly_sales = (
    sales
    .groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
    .sum()
    .reset_index()
)

forecast_data = monthly_sales.rename(columns={"Order Date": "ds", "Sales": "y"})

model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
model.fit(forecast_data)

future = model.make_future_dataframe(periods=6, freq="ME")
forecast = model.predict(future)

result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(6).copy()

result.columns = ["Month", "Expected Demand", "Minimum Demand", "Maximum Demand"]
result["Month"] = result["Month"].dt.strftime("%B %Y")

result["Expected Demand"] = result["Expected Demand"].round(0).astype(int)
result["Minimum Demand"] = result["Minimum Demand"].round(0).astype(int)
result["Maximum Demand"] = result["Maximum Demand"].round(0).astype(int)

print("\nRaritone AI Forecast Report: Next 6 Months Demand Outlook\n")
print(result.to_string(index=False))

fig = model.plot(forecast)
ax = fig.gca()

fig.set_size_inches(12, 6)

fig.suptitle(
    "Raritone AI Demand Intelligence Dashboard",
    fontsize=18,
    fontweight="bold",
    y=0.96
)

ax.set_title(
    "Fashion Demand Forecast (Next 6 Months Outlook)",
    fontsize=14,
    pad=15
)

ax.set_xlabel("Timeline (Monthly View)", fontsize=12)
ax.set_ylabel("Expected Customer Demand", fontsize=12)

ax.axvspan(
    forecast["ds"].iloc[-6],
    forecast["ds"].iloc[-1],
    color="orange",
    alpha=0.15
)

ax.grid(True, linestyle="--", alpha=0.4)

plt.subplots_adjust(top=0.88)
plt.tight_layout()

plt.show()

fig2 = model.plot_components(forecast)

for ax in fig2.axes:
    ax.grid(True, linestyle="--", alpha=0.3)

fig2.suptitle(
    "Raritone AI Demand Drivers (Trend & Seasonality Insights)",
    fontsize=16,
    fontweight="bold",
    y=0.96
)

plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.show()