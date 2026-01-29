import pandas as pd
import joblib

model = joblib.load("model/implementation_effort_model.pkl")


def predict_implementation(form_data: dict):
    # 1. Read CSV header as schema
    schema = pd.read_csv("data/Implementation_testing.csv", nrows=0).columns.tolist()

    excluded_cols = {
        "Feature_ID",
        "Final_Effort_Hours",
        "Estimated_Implementation_Effort"
    }

    model_columns = [c for c in schema if c.strip() not in excluded_cols]

    # 2. Build row using CSV column names
    row = {}
    for col in model_columns:
        clean_col = col.strip()
        if clean_col not in form_data:
            raise ValueError(f"Missing feature: {clean_col}")
        raw_value = form_data.get(clean_col, "").strip()

        if raw_value == "":
            row[col] = 0.0
        else:
            try:
                row[col] = float(raw_value)
            except ValueError:
                raise ValueError(f"Invalid numeric value for {clean_col}: {raw_value}")

    # 3. Create DataFrame
    input_df = pd.DataFrame([row], columns=model_columns)

    # 🔑 4. FORCE column names to match model training schema
    input_df.columns = model.feature_names_in_

    # 5. Predict
    return model.predict(input_df)[0]
