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
            feature_id = form_data.pop("Feature_ID")
            form_data.pop("estimate")

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

    if "search" in request.form:
        feature_id = request.form["Feature_ID"]
        data = fetch_by_feature_id("data/Implementation_testing.csv", feature_id)

        if not data:
            error = "Feature_ID not found"

    elif "update" in request.form:
        try:
            feature_id = request.form["Feature_ID"]
            final_hours = request.form["Final_Effort_Hours"]
            
            if final_hours == "" or final_hours is None:
                raise ValueError("Final_Effort_Hours cannot be empty")
            
            update_final_effort("data/Implementation_testing.csv", feature_id, final_hours)
        except Exception as e:
            error = str(e)

    elif "estimate" in request.form:
        try:
            form_data = dict(request.form)
            feature_id = form_data.pop("Feature_ID")
            form_data.pop("estimate")

            prediction = predict_implementation(form_data)

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
