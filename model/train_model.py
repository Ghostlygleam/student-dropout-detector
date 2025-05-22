import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Selected features
USED_FEATURES = [
    "Gender", "Age at enrollment", "Marital Status", "Course",
    "Admission grade", "Scholarship holder", "Debtor", "Tuition fees up to date",
    "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (enrolled)", "Curricular units 2nd sem (approved)", "Curricular units 2nd sem (grade)"
]

# Load and filter dataset
df = pd.read_csv("data/students_dropout_academic_success.csv")
df = df[USED_FEATURES + ["target"]]

# Encode course (remove code, convert to string)
df["Course"] = df["Course"].astype(str)

# One-hot encoding
X = pd.get_dummies(df.drop(columns=["target"]))
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, "model/dropout_model.pkl")
print("✅ Model saved to: model/dropout_model.pkl")
