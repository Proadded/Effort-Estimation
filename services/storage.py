import pandas as pd

def fetch_by_feature_id(csv_path: str, feature_id: str):
    df = pd.read_csv(csv_path)

    row = df[df["Feature_ID"] == feature_id]

    if row.empty:
        return None

    return row.iloc[0].to_dict()

def update_final_effort(csv_path: str, feature_id: str, final_hours):
    df = pd.read_csv(csv_path)

    if feature_id not in df["Feature_ID"].values:
        raise ValueError("Feature_ID not found")

    df.loc[df["Feature_ID"] == feature_id, "Final_Effort_Hours"] = final_hours

    df.to_csv(csv_path, index=False)


def append_to_csv(csv_path: str, incoming_row: dict):
    df = pd.read_csv(csv_path)

    # Build mapping: stripped_name -> actual_csv_column
    column_map = {col.strip(): col for col in df.columns}

    final_row = {}

    for key, value in incoming_row.items():
        if key in column_map:
            final_row[column_map[key]] = value
        else:
            raise ValueError(f"Column '{key}' not found in CSV")

    # Ensure all columns exist (fill missing with empty)
    for col in df.columns:
        if col not in final_row:
            final_row[col] = ""

    df = pd.concat([df, pd.DataFrame([final_row])], ignore_index=True)
    df.to_csv(csv_path, index=False)
