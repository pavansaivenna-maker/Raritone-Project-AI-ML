from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import time

app = FastAPI(title="Fashion-AI Analytics APIs", version="1.0")

# Mock Database for speed
analytics_db = {
    "try_on_events": [],
    "user_engagement": [],
    "conversions": []
}

# Pydantic Models for Input Validation
class TryOnEvent(BaseModel):
    user_id: str
    garment_id: str
    processing_time_ms: int
    success: bool

class EngagementEvent(BaseModel):
    user_id: str
    session_duration_seconds: int
    retry_attempts: int

class ConversionEvent(BaseModel):
    user_id: str
    garment_id: str
    added_to_cart: bool

@app.post("/api/v1/analytics/try-on")
async def log_try_on(event: TryOnEvent):
    """Logs Virtual Try-On Analytics"""
    analytics_db["try_on_events"].append(event.dict())
    return {"status": "success", "message": "Try-on analytics logged."}

@app.post("/api/v1/analytics/engagement")
async def log_engagement(event: EngagementEvent):
    """Logs User Engagement Analytics"""
    analytics_db["user_engagement"].append(event.dict())
    return {"status": "success", "message": "Engagement analytics logged."}

@app.post("/api/v1/analytics/conversion")
async def log_conversion(event: ConversionEvent):
    """Logs Conversion Analytics"""
    analytics_db["conversions"].append(event.dict())
    return {"status": "success", "message": "Conversion analytics logged."}

@app.get("/api/v1/analytics/dashboard")
async def get_dashboard_metrics():
    """Returns aggregated data for the Analytics Dashboard"""
    total_try_ons = len(analytics_db["try_on_events"])
    total_conversions = sum(1 for e in analytics_db["conversions"] if e["added_to_cart"])
    
    conversion_rate = (total_conversions / total_try_ons * 100) if total_try_ons > 0 else 0
    
    return {
        "total_try_ons": total_try_ons,
        "total_conversions": total_conversions,
        "conversion_rate_percentage": round(conversion_rate, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)