import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Encode size (S, M, L, XL)
encoder = LabelEncoder()
df["size"] = encoder.fit_transform(df["size"])

# Features
X = df[["height", "weight", "size"]]

# Target
y = df["fit"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Model validation
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")

# Save model and encoder
joblib.dump(model, "fit_model.pkl")
joblib.dump(encoder, "size_encoder.pkl")

print("Model and encoder saved successfully")