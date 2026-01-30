import pandas as pd
import joblib

model = joblib.load("model/grooming_effort_model.pkl")


def predict_grooming(form_data: dict):
    import pandas as pd

    model_columns = list(model.feature_names_in_)

    row = {}

    for col in model_columns:
        clean_col = col.strip()
        raw_value = form_data.get(clean_col, "").strip()

        if raw_value == "":
            row[col] = 0.0
        else:
            row[col] = float(raw_value)

    input_df = pd.DataFrame([row], columns=model_columns)

    return model.predict(input_df)[0]
