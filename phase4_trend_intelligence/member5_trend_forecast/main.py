from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Trend Forecasting API")

model = joblib.load("trend_model.pkl")
encoders = joblib.load("trend_encoders.pkl")

class TrendRequest(BaseModel):
    season: str
    category: str
    color: str
    style: str
    trend_score: float

@app.get("/")
def home():
    return {"message": "Trend Forecasting API is Running"}

@app.post("/predict-trend")
def predict_trend(request: TrendRequest):
    data = pd.DataFrame({
        "season": [encoders["season"].transform([request.season])[0]],
        "category": [encoders["category"].transform([request.category])[0]],
        "color": [encoders["color"].transform([request.color])[0]],
        "style": [encoders["style"].transform([request.style])[0]],
        "trend_score": [request.trend_score]
    })

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0].max()

    return {
        "season": request.season,
        "category": request.category,
        "color": request.color,
        "style": request.style,
        "trend_score": request.trend_score,
        "is_trending": prediction,
        "confidence": f"{probability * 100:.2f}%"
    }

@app.get("/trending-colors")
def trending_colors(season: str = "Summer"):
    df = pd.read_csv("dataset.csv")
    filtered = df[df["season"] == season]
    color_trends = filtered.groupby("color")["trend_score"].mean().sort_values(ascending=False)
    top_colors = color_trends.head(5).reset_index()
    return {
        "season": season,
        "trending_colors": [
            {"color": row["color"], "avg_trend_score": round(row["trend_score"], 2)}
            for _, row in top_colors.iterrows()
        ]
    }

@app.get("/trending-styles")
def trending_styles(season: str = "Summer"):
    df = pd.read_csv("dataset.csv")
    filtered = df[df["season"] == season]
    style_trends = filtered.groupby("style")["trend_score"].mean().sort_values(ascending=False)
    top_styles = style_trends.reset_index()
    return {
        "season": season,
        "trending_styles": [
            {"style": row["style"], "avg_trend_score": round(row["trend_score"], 2)}
            for _, row in top_styles.iterrows()
        ]
    }

@app.get("/seasonal-analysis")
def seasonal_analysis():
    df = pd.read_csv("dataset.csv")
    result = {}
    for season in df["season"].unique():
        season_df = df[df["season"] == season]
        result[season] = {
            "total_products": len(season_df),
            "trending_count": len(season_df[season_df["is_trending"] == "Yes"]),
            "avg_trend_score": round(season_df["trend_score"].mean(), 2),
            "top_color": season_df.groupby("color")["trend_score"].mean().idxmax(),
            "top_style": season_df.groupby("style")["trend_score"].mean().idxmax(),
            "top_category": season_df.groupby("category")["trend_score"].mean().idxmax()
        }
    return {"seasonal_analysis": result}
