import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("size_dataset.csv")

# Encode Gender
gender_encoder = LabelEncoder()
data["Gender"] = gender_encoder.fit_transform(data["Gender"])

# Encode Size
size_encoder = LabelEncoder()
data["Size"] = size_encoder.fit_transform(data["Size"])

# Features
X = data[["Height", "Weight", "Chest", "Waist", "Hip", "Gender"]]

# Target
y = data["Size"]

# Train Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X, y)

# Save files
joblib.dump(model, "size_model.pkl")
joblib.dump(gender_encoder, "gender_encoder.pkl")
joblib.dump(size_encoder, "size_encoder.pkl")

print("Model Saved Successfully!")