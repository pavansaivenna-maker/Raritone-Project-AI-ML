from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="AI Size Recommendation API")

# Load model and encoders
model = joblib.load("size_model.pkl")
gender_encoder = joblib.load("gender_encoder.pkl")
size_encoder = joblib.load("size_encoder.pkl")

class UserInput(BaseModel):
    height: float
    weight: float
    chest: float
    waist: float
    hip: float
    gender: str

@app.post("/predict_size")
def predict_size(user: UserInput):

    gender_value = gender_encoder.transform([user.gender])[0]

    input_data = pd.DataFrame([[
        user.height,
        user.weight,
        user.chest,
        user.waist,
        user.hip,
        gender_value
    ]], columns=[
        "Height",
        "Weight",
        "Chest",
        "Waist",
        "Hip",
        "Gender"
    ])

    prediction = model.predict(input_data)

    size = size_encoder.inverse_transform(prediction)

    return {
    "height": user.height,
    "weight": user.weight,
    "gender": user.gender,
    "recommended_size": size[0],
    "model": "Random Forest"
}