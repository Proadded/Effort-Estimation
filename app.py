from flask import Flask, render_template, request
from services.grooming_estimator import predict_grooming
from services.implementation_estimator import predict_implementation
from services.storage import append_to_csv
from services.storage import fetch_by_feature_id, update_final_effort

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/grooming", methods=["GET", "POST"])
def grooming():
    prediction = None
    error = None
    data = None

    if "search" in request.form:
        feature_id = request.form["Feature_ID"]
        data = fetch_by_feature_id("data/Grooming_testing.csv", feature_id)

        if not data:
            error = "Feature_ID not found"

    elif "update" in request.form:
        try:
            feature_id = request.form["Feature_ID"]
            final_hours = request.form["Final_Effort_Hours"]
            if final_hours == "" or final_hours is None:
                raise ValueError("Final_Effort_Hours cannot be empty")
            
            update_final_effort("data/Grooming_testing.csv", feature_id, final_hours)
        except Exception as e:
            error = str(e)

    elif "estimate" in request.form:
        try:
            form_data = dict(request.form)

            # Remove non-feature keys
            feature_id = form_data.pop("Feature_ID", None)
            form_data.pop("estimate", None)
            form_data.pop("update", None)
            form_data.pop("Final_Effort_Hours", None)

            prediction = predict_grooming(form_data)

            row = {
                "Feature_ID": feature_id,
                **form_data,
                "Estimated_Grooming_Effort": prediction
            }

            append_to_csv("data/Grooming_testing.csv", row)

        except Exception as e:
            error = str(e)

    return render_template(
        "grooming.html",
        prediction=prediction,
        error=error,
        data=data
    )
    
@app.route("/implementation", methods=["GET", "POST"])
def implementation():
    prediction = None
    error = None
    data = None

    # ---------------- SEARCH ----------------
    if "search" in request.form:
        feature_id = request.form["Feature_ID"]
        data = fetch_by_feature_id("data/Implementation_testing.csv", feature_id)

        if not data:
            error = "Feature_ID not found"

    # ---------------- UPDATE FINAL HOURS ----------------
    elif "update" in request.form:
        try:
            feature_id = request.form["Feature_ID"]
            final_hours = request.form.get("Final_Effort_Hours")

            if final_hours is None or final_hours == "":
                raise ValueError("Final_Effort_Hours cannot be empty")

            update_final_effort(
                "data/Implementation_testing.csv",
                feature_id,
                final_hours
            )

        except Exception as e:
            error = str(e)

    # ---------------- ESTIMATE ----------------
    elif "estimate" in request.form:
        try:
            # Copy form data
            form_data = dict(request.form)

            # Extract & remove non-feature fields
            feature_id = form_data.pop("Feature_ID", None)
            form_data.pop("estimate", None)
            form_data.pop("update", None)
            form_data.pop("Final_Effort_Hours", None)

            # 🔑 Option 2: CSV-driven schema alignment happens INSIDE this call
            prediction = predict_implementation(form_data)

            # Append estimation result
            row = {
                "Feature_ID": feature_id,
                **form_data,
                "Estimated_Implementation_Effort": prediction
            }

            append_to_csv("data/Implementation_testing.csv", row)

        except Exception as e:
            error = str(e)

    return render_template(
        "implementation.html",
        prediction=prediction,
        error=error,
        data=data
    )


@app.route("/debug/csv/<name>")
def debug_csv(name):
    if name not in ["Grooming_testing", "Implementation_testing"]:
        return "Invalid file", 400

    with open(f"data/{name}.csv", "r") as f:
        return "<pre>" + f.read() + "</pre>"



if __name__ == "__main__":
    app.run(port=5000, debug=True)
