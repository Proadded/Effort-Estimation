import pandas as pd
import joblib

# Load model once
model = joblib.load("model/implementation_effort_model.pkl")


def predict_implementation(form_data: dict):
    import pandas as pd

    # 🔑 Use model schema ONLY (NOT CSV)
    model_columns = list(model.feature_names_in_)

    row = {}

    for col in model_columns:
        clean_col = col.strip()
        raw_value = form_data.get(clean_col, "").strip()

        if raw_value == "":
            row[col] = 0.0
        else:
            try:
                row[col] = float(raw_value)
            except ValueError:
                raise ValueError(
                    f"Invalid numeric value for {clean_col}: {raw_value}"
                )

    input_df = pd.DataFrame([row], columns=model_columns)

    return model.predict(input_df)[0]
