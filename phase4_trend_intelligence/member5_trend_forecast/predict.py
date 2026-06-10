import pandas as pd
import joblib

model = joblib.load("trend_model.pkl")
encoders = joblib.load("trend_encoders.pkl")

season = "Summer"
category = "Tops"
color = "Red"
style = "Casual"
trend_score = 85

data = pd.DataFrame({
    "season": [encoders["season"].transform([season])[0]],
    "category": [encoders["category"].transform([category])[0]],
    "color": [encoders["color"].transform([color])[0]],
    "style": [encoders["style"].transform([style])[0]],
    "trend_score": [trend_score]
})

prediction = model.predict(data)
print("Is Trending:", prediction[0])