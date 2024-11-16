from flask import Flask, render_template, request
from database import db_cursor, db
import datetime

# Creating an app that runs the entire localhost server
app = Flask(__name__)


# Some test stuff
# ========================

# ========================

# ROUTES FOR DISPLAYING PAGES

# index.html
# ========================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
# ========================


# calibration.html
# ========================
@app.route('/calibration', methods=["GET"])
def calibration():
    return render_template("calibration.html")
# ========================


# test_code.html
# ========================
@app.route("/test_code", methods=["GET"])
def test_code():
    return render_template("test_code.html")
# ========================

# ROUTES FOR PROCESSING DATA WITH AJAX

# /store gets the list of 20 dictionaries which have the following structure:
# {x: float, y: float, t: float}
# ========================
@app.route("/store", methods=["POST"])
def store():
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    for dictionary in request.json:
        db_cursor.execute(
            "INSERT INTO solve_table (Student_Email, Task_Name, Gaze_X, Gaze_Y, Gaze_Time) VALUES (%s, %s, %s, %s, %s)",
            (dictionary['student_email'], dictionary['task'], dictionary['x'], dictionary['y'], f"{dictionary['t']} {today}")
        )
        db.commit()
    return "200"
# ========================


if __name__ == "__main__":
    app.run(debug=True)
