import joblib
import pandas as pd
import os

model_path = os.path.join(os.path.dirname(__file__), "../model/implementation_effort_model.pkl")
model = joblib.load(model_path)
MODEL_FEATURES = model.get_booster().feature_names

def predict_implementation(inputs: dict) -> float:
    mapped = {}

    for feature in MODEL_FEATURES:
        clean = feature.strip()
        if clean not in inputs:
            raise ValueError(f"Missing feature: {clean}")
        mapped[feature] = float(inputs[clean])

    df = pd.DataFrame(
        [[mapped[f] for f in MODEL_FEATURES]],
        columns=MODEL_FEATURES
    )

    return float(model.predict(df)[0])

