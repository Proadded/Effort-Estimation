import pandas as pd
import joblib

model = joblib.load("model/implementation_effort_model.pkl")


def predict_implementation(form_data: dict):
    """
    Option-2 (CSV-driven) with normalization adapter.
    Model is immutable. CSV stays unchanged.
    """

    # 1. Read CSV schema
    raw_schema = pd.read_csv("data/Implementation_testing.csv", nrows=0).columns.tolist()

    # 2. Columns not used by model
    excluded = {
        "Feature_ID",
        "Final_Effort_Hours",
        "Estimated_Implementation_Effort"
    }

    # 3. Build normalized schema (strip spaces)
    model_columns = []
    column_map = {}  # clean_name -> original_csv_name

    for col in raw_schema:
        clean = col.strip()
        if clean not in excluded:
            model_columns.append(clean)
            column_map[clean] = col  # map clean → dirty

    # 4. Build row using CLEAN names (model expects these)
    row = {}

    for feature in model_columns:
        if feature not in form_data:
            raise ValueError(f"Missing feature: {feature}")

        try:
            row[feature] = float(form_data[feature])
        except ValueError:
            raise ValueError(f"Invalid numeric value for {feature}: {form_data[feature]}")

    # 5. Create DataFrame with CLEAN column names
    input_df = pd.DataFrame([row], columns=model_columns)

    # 6. Predict
    return model.predict(input_df)[0]
