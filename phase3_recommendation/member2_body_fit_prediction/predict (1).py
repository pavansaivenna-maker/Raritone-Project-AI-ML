import pandas as pd
import joblib

model = joblib.load("fit_model.pkl")
encoder = joblib.load("size_encoder.pkl")

height = 170
weight = 65
size = "M"

size_encoded = encoder.transform([size])[0]

data = pd.DataFrame({
    "height": [height],
    "weight": [weight],
    "size": [size_encoded]
})

prediction = model.predict(data)
print("Predicted Fit:", prediction[0])