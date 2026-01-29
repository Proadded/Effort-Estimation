import pandas as pd
import joblib

# Load model once
model = joblib.load("model/implementation_effort_model.pkl")


def predict_implementation(form_data: dict):
    """
    CSV-driven schema adapter (Option 2).
    Model remains immutable.
    Handles:
    - trailing spaces
    - column order
    - missing values
    - strict feature-name matching
    """

    # 1. Read CSV header as schema (SOURCE OF TRUTH)
    schema = pd.read_csv(
        "data/Implementation_testing.csv",
        nrows=0
    ).columns.tolist()

    # 2. Exclude non-model columns
    excluded_cols = {
        "Feature_ID",
        "Final_Effort_Hours",
        "Estimated_Implementation_Effort"
    }

    model_columns = [c for c in schema if c.strip() not in excluded_cols]

    # 3. Build row using CSV column names
    row = {}

    for col in model_columns:
        clean_col = col.strip()
        raw_value = form_data.get(clean_col, "").strip()

        # Default empty values to 0
        if raw_value == "":
            row[col] = 0.0
        else:
            try:
                row[col] = float(raw_value)
            except ValueError:
                raise ValueError(
                    f"Invalid numeric value for {clean_col}: {raw_value}"
                )

    # 4. Create DataFrame with CSV ordering
    input_df = pd.DataFrame([row], columns=model_columns)

    # 🔑 5. FORCE column names to EXACT model training schema
    # (this fixes the trailing-space mismatch)
    input_df.columns = model.feature_names_in_

    # 6. Predict
    return model.predict(input_df)[0]
