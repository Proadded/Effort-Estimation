import pandas as pd
import joblib

model = joblib.load("model/grooming_effort_model.pkl")


def predict_grooming(form_data: dict):
    import pandas as pd

    # 1. Read CSV header
    schema = pd.read_csv("data/Grooming_testing.csv", nrows=0).columns.tolist()

    excluded_cols = {
        "Feature_ID",
        "Final_Effort_Hours",
        "Estimated_Grooming_Effort"
    }

    model_columns = [c for c in schema if c.strip() not in excluded_cols]

    # 2. Build row using CLEAN keys → CSV names
    row = {}
    for col in model_columns:
        clean_col = col.strip()
        raw_value = form_data.get(clean_col, "").strip()

        if raw_value == "":
            row[col] = 0.0
        else:
            row[col] = float(raw_value)

    # 3. Build DataFrame
    input_df = pd.DataFrame([row], columns=model_columns)

    # 🔑 4. FORCE model-trained feature names (THIS WAS MISSING)
    input_df.columns = model.feature_names_in_

    # 5. Predict
    return model.predict(input_df)[0]
