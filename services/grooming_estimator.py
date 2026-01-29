import pandas as pd
import joblib

model = joblib.load("model/grooming_effort_model.pkl")


def predict_grooming(form_data: dict):
    """
    CSV-driven schema adapter (Option 2).
    Model is treated as immutable.
    """

    # 1. Read grooming CSV header as schema
    schema = pd.read_csv("data/Grooming_testing.csv", nrows=0).columns.tolist()

    # 2. Exclude non-model columns
    excluded_cols = {
        "Feature_ID",
        "Final_Effort_Hours",
        "Estimated_Grooming_Effort"
    }

    model_columns = [c for c in schema if c.strip() not in excluded_cols]

    # 3. Build model-aligned row
    row = {}

    for col in model_columns:
        clean_col = col.strip()

        if clean_col not in form_data:
            raise ValueError(f"Missing feature: {clean_col}")

        value = form_data[clean_col]

        try:
            row[col] = float(value)
        except ValueError:
            raise ValueError(f"Invalid numeric value for {clean_col}: {value}")

    # 4. Ordered DataFrame (matches training)
    input_df = pd.DataFrame([row], columns=model_columns)

    # 5. Predict
    return model.predict(input_df)[0]
