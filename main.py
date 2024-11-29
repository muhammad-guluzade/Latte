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
            

# ROUTES FOR PROCESSING DATA WITH AJAX

# For now, /store is the only one method in the website used with AJAX
# in order to store the gaze into the database.
# It receives a list of 20 dictionaries, and stores the received data
# into Record->Fixation table inside Latte database.
# ========================
@app.route("/store", methods=["POST"])
def store():
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    db_cursor.execute(
        "INSERT INTO Record (Student_id, Task_id) VALUES (%s, %s)",
        (request.json[0]["student_id"], request.json[0]["task_id"])
    )
    db_cursor.execute("SELECT LAST_INSERT_ID()")
    id = db_cursor.fetchone()[0]
    for dictionary in request.json:
        db_cursor.execute(
            "INSERT INTO Fixation (Gaze_X, Gaze_Y, Gaze_Time, Record_id) VALUES (%s, %s, %s, %s)",
            (dictionary['x'], dictionary['y'], f"{dictionary['t']} {today}", id)
        )
    db.commit()
    return "200"
# ========================


if __name__ == "__main__":
    app.run(debug=True)
