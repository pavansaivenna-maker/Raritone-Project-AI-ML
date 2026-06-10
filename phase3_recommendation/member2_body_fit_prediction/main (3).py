from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Body Fit Prediction API")

model = joblib.load("fit_model.pkl")
encoder = joblib.load("size_encoder.pkl")

class FitRequest(BaseModel):
    height: float
    weight: float
    size: str

@app.get("/")
def home():
    return {"message": "Body Fit Prediction API is Running"}

@app.post("/predict")
def predict_fit(request: FitRequest):
    size_encoded = encoder.transform([request.size])[0]
    
    data = pd.DataFrame({
        "height": [request.height],
        "weight": [request.weight],
        "size": [size_encoded]
    })
    
    prediction = model.predict(data)[0]
    
    return {
        "height": request.height,
        "weight": request.weight,
        "size": request.size,
        "predicted_fit": prediction
    }