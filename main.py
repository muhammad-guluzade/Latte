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
    sql = "INSERT INTO solve_table (Student_Email, Task_Name, Gaze_X, Gaze_Y, Gaze_Time) VALUES (%s, %s, %s, %s, %s)"
    val = ("e254595@metu.edu.tr", "Coding Task 1", "500", "400", "12:45:55.454")
    db_cursor.execute(sql, val)
    db.commit()
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
# It then stores the x, y coordinates, and time in seconds starting from 01/01/1970
# in order to have unique time for each gaze point.
# It stores details in details.txt for now.
# ========================
@app.route("/store", methods=["POST"])
def store():
    with open("details.txt", "a+") as file:
        for dictionary in request.json:
            file.write(f"X: {dictionary['x']}, Y: {dictionary['y']}, Time: {dictionary['t']}s\n")
    return "200"
# ========================


if __name__ == "__main__":
    app.run(debug=True)
