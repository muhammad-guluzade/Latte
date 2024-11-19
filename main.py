from flask import Flask, render_template, request, redirect
from database import db_cursor, db
import datetime

# Creating an app that runs the entire localhost server
app = Flask(__name__)


# Some test stuff
# ========================

# ========================

# GET ROUTES (FOR DISPLAYING PAGES)

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

# POST ROUTES (TO STORE THE DATA INTO DATABASE)

# Test route for saving either course, task set, or task
# ========================
@app.route("/create_c_ts_t", methods=["GET", "POST"])
def create_task_or_set_of_tasks_or_course():
    if request.method == "GET":
        # C - Course (1)
        # TS - Task Set (2)
        # T - Task (3)
        C_TS_T = 3
        return render_template("c_ts_t_temp.html", c_ts_t=C_TS_T)
    else:
        if len(request.form) == 1:
            db_cursor.execute("INSERT INTO SetOfTask (Name) VALUES (%s)", (request.form.get("set_of_task_name"),))
        elif len(request.form) == 2:
            db_cursor.execute("INSERT INTO Course (Name, Description) VALUES (%s, %s)", (request.form.get("course_name"), request.form.get("course_description")))
        else:
            db_cursor.execute("INSERT INTO Task (Name, Description, Answer) VALUES (%s, %s, %s)", (request.form.get("task_name"), request.form.get("task_description"), request.form.get("task_answer")))
        db.commit()
        return redirect("/create_c_ts_t")
# ========================
            

# ROUTES FOR PROCESSING DATA WITH AJAX

# For now, /store is the only one method in the website used with AJAX
# in order to store the gaze into the database.
# It receives a list of 20 dictionaries, and stores the received data
# into solve_table table inside Latte database.
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
