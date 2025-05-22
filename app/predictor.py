import pandas as pd
import joblib

model = joblib.load("model/dropout_model.pkl")

def predict_dropout(input_df: pd.DataFrame) -> pd.DataFrame:
    df = input_df.copy()
    df["Course"] = df["Course"].astype(str)
    df_encoded = pd.get_dummies(df)

    for col in model.feature_names_in_:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[model.feature_names_in_]

    pred = model.predict(df_encoded)
    proba = model.predict_proba(df_encoded)

    result = df.copy()
    result["Prediction"] = pred
    for idx, cls in enumerate(model.classes_):
        result[f"{cls} (%)"] = (proba[:, idx] * 100).round(1)

    return result
