import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Load Dataset
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

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# --------------------
# Decision Tree
# --------------------
dt_model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)

dt_model.fit(X_train, y_train)

dt_pred = dt_model.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_pred)

# --------------------
# Random Forest
# --------------------
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

# --------------------
# New Customer Prediction
# --------------------
new_customer = pd.DataFrame(
    [[170, 65, 38, 32, 40, 0]],
    columns=["Height", "Weight", "Chest", "Waist", "Hip", "Gender"]
)

prediction = rf_model.predict(new_customer)

recommended_size = size_encoder.inverse_transform(prediction)

# --------------------
# Results
# --------------------
print("\n===== MODEL RESULTS =====")

print(f"Decision Tree Accuracy : {dt_accuracy:.2f}")
print(f"Random Forest Accuracy : {rf_accuracy:.2f}")

print("\nRecommended Size :", recommended_size[0])

print("\nRandom Forest Confusion Matrix:")
print(confusion_matrix(y_test, rf_pred))