import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

print("AI Fashion Trend Forecasting System Initializing...")

sales = pd.read_csv("fashion_retail_sales.csv")

print("Dataset Loaded:", sales.shape)

sales = sales.fillna("")

sales["Date Purchase"] = pd.to_datetime(sales["Date Purchase"], errors="coerce")
sales["Purchase Amount (Rupees)"] = pd.to_numeric(
    sales["Purchase Amount (Rupees)"],
    errors="coerce"
)

sales = sales.dropna(subset=["Date Purchase", "Purchase Amount (Rupees)"])

monthly_sales = (
    sales
    .groupby(pd.Grouper(key="Date Purchase", freq="ME"))["Purchase Amount (Rupees)"]
    .sum()
    .reset_index()
)

forecast_data = monthly_sales.rename(columns={
    "Date Purchase": "ds",
    "Purchase Amount (Rupees)": "y"
})

model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
model.fit(forecast_data)

future = model.make_future_dataframe(periods=6, freq="ME")
forecast = model.predict(future)

result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(6).copy()

result.columns = ["Month", "Expected Sales", "Minimum Estimate", "Maximum Estimate"]
result["Month"] = result["Month"].dt.strftime("%B %Y")

result = result.round(0)
result[["Expected Sales", "Minimum Estimate", "Maximum Estimate"]] = result[
    ["Expected Sales", "Minimum Estimate", "Maximum Estimate"]
].astype(int)

print("\nAI Fashion Sales Forecast Report (Next 6 Months)\n")
print(result.to_string(index=False))

fig = model.plot(forecast)
ax = fig.gca()

fig.set_size_inches(12, 6)

fig.suptitle(
    "Fashion AI Demand Intelligence Dashboard",
    fontsize=18,
    fontweight="bold",
    y=0.96
)

ax.set_title(
    "Revenue Trend Forecast (Next 6 Months Projection)",
    fontsize=14,
    pad=15
)

ax.set_xlabel("Time (Monthly)", fontsize=12)
ax.set_ylabel("Predicted Revenue (₹)", fontsize=12)

ax.axvspan(
    forecast["ds"].iloc[-6],
    forecast["ds"].iloc[-1],
    color="green",
    alpha=0.12
)

ax.grid(True, linestyle="--", alpha=0.4)

plt.subplots_adjust(top=0.88)
plt.tight_layout()
plt.show()

fig2 = model.plot_components(forecast)

for ax in fig2.axes:
    ax.grid(True, linestyle="--", alpha=0.3)

fig2.suptitle(
    "Key Drivers of Fashion Sales (Trend + Seasonality Breakdown)",
    fontsize=16,
    fontweight="bold",
    y=0.96
)

plt.subplots_adjust(top=0.88)
plt.tight_layout()
plt.show()