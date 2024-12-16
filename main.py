from functools import wraps
from flask import Flask, render_template, request, redirect, session
# from database import cursor, db
import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter, ImageFormatter
from pygments.lexers import CLexer, JavaLexer
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


# CHANGE TO MYSQL AFTER
# =========================
import sqlite3
conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()
# =========================

# Creating an app that runs the entire localhost server
app = Flask(__name__)
app.secret_key = "123"
PLACEHOLDER = "?"
LEXER = JavaLexer()


# Some test stuff
# ========================

# ========================

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "latte_user" not in session:
            return redirect("/")  # Redirect to the index route ("/")
        return func(*args, **kwargs)
    return decorated_function


def instructor_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_type" not in session:
            return redirect("/")
        if session["user_type"] != "i":
            return redirect("/")  # Redirect to the index route ("/")
        return func(*args, **kwargs)
    return decorated_function

# GET AND POST ROUTES

# index.html
# ========================
@app.route("/", methods=["GET"])
def index():
    if "latte_user" not in session:
        return render_template("pages/login.html")
    if session['user_type'] == "a":
        return render_template("pages/admin_panel.html")
    if session['user_type'] == "i":
        return render_template("pages/dashboardi.html")
    else:
        course_codes_for_student = [item[0] for item in cursor.execute(f"SELECT course_code FROM StudentCourseTable WHERE student_username='{session['latte_user']}'").fetchall()]
        return render_template("pages/dashboards.html", courses=course_codes_for_student)
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

# ========================
@app.route("/add_students_to_course", methods=["GET", "POST"])
@login_required
@instructor_only
def add_students_to_course():
    if request.method == "POST":
        if cursor.execute(f"SELECT student_username, course_code FROM StudentCourseTable WHERE student_username='{request.form.get('singleStudent')}' AND course_code='{request.form.get('courseSelect')}'").fetchone():
            return "Student already added to this course"
        cursor.execute(
            "INSERT INTO StudentCourseTable (student_username, course_code) VALUES (?, ?)",
            (request.form.get("singleStudent"), request.form.get("courseSelect")),
        )
        conn.commit()
        return redirect("/add_students_to_course")
    courses = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE Instructor_username='{session['latte_user']}'").fetchall()]
    students = [item[0] for item in cursor.execute("SELECT student_username FROM Student").fetchall()]

    return render_template("pages/add_students_to_course.html", courses=courses, students=students)
# ========================


# ========================
@app.route("/course_details/<course_code>", methods=["GET", "POST"])
@login_required
@instructor_only
def course_details(course_code):
    if request.method == "POST":
        cursor.execute(
            f"UPDATE Course SET Name={PLACEHOLDER}, Description={PLACEHOLDER} WHERE course_code='{course_code}'",
            (request.form.get("courseName"), request.form.get("courseDescription"))
        )
        conn.commit()
        return redirect("/view_courses")
    course = cursor.execute(f"SELECT name, description, course_code FROM Course WHERE course_code='{course_code}'").fetchone()
    if not course:
        return "Course not found"
    return render_template("pages/course_details.html", course=course)
# ========================

# ========================
@app.route("/create_course", methods=["GET", "POST"])
@login_required
@instructor_only
def create_course():
    students = [item[0] for item in cursor.execute(f"SELECT student_username FROM Student").fetchall()]
    if request.method == "GET":
        return render_template("pages/create_course.html", students=students)

    cursor.execute(
        f"INSERT INTO Course (Course_code, Name, Description, Instructor_username) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("courseCode"), request.form.get("courseName"), request.form.get("courseDescription"), session['latte_user'])
    )

    if request.form.get("addTaskSet"):
        cursor.execute(
            f"INSERT INTO SetOfTask (Name, Course_code) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
            (request.form.get("taskSetName"), request.form.get("courseCode"))
        )
        set_of_task_id = cursor.lastrowid

    if request.form.get("addTasks"):
        cursor.execute(
            f"INSERT INTO Task (Name, Description, Set_of_task_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
            (request.form.get("taskName"), request.form.get("taskDescription"), set_of_task_id)
        )

    if request.form.get("addStudents"):
        if request.form.get("studentType") == "single":
            cursor.execute(
                "INSERT INTO StudentCourseTable (student_username, course_code) VALUES (?, ?)",
                (request.form.get("singleStudent"), request.form.get("courseCode")),
            )

    conn.commit()

    return render_template("pages/create_course.html", msg="Course created successfully", students=students)

# ========================

# ========================
@app.route("/generate_report", methods=["GET", "POST"])
@login_required
@instructor_only
def generate_report():
    students = [item[0] for item in cursor.execute("SELECT student_username FROM Student").fetchall()]
    if request.method == "GET":
        return render_template("pages/generate_report.html", students=students)
    data = cursor.execute(f"SELECT task_id, student_username, time FROM TaskDimensions WHERE student_username='{request.form.get('individualStudent')}'").fetchone()
    return redirect(f"/generate_heatmap/{data[1]}/{data[0]}/{data[2].split()[0]}+{data[2].split()[1].replace('/', '-')}")
# ========================

# ========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/login.html")

    password = cursor.execute(f"SELECT password FROM User WHERE username='{request.form.get('username')}'").fetchone()

    if not password:
        return render_template("pages/login.html", msg="The user does not exist")

    if password[0] != request.form.get("password"):
        return render_template("pages/login.html", msg="Passwords do not match")

    admins_usernames = [item[0] for item in cursor.execute("SELECT admin_username FROM Admin").fetchall()]
    instructors_usernames = [item[0] for item in cursor.execute("SELECT instructor_username FROM Instructor").fetchall()]

    if request.form.get("username") in admins_usernames:
        session["user_type"] = "a"
    elif request.form.get("username") in instructors_usernames:
        session["user_type"] = "i"
    else:
        session["user_type"] = "s"
    session["latte_user"] = f"{request.form.get('username')}"

    return redirect("/")


# ========================

# ========================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("pages/signup.html")

    if request.args.get("admin") == "true":
        if session['user_type'] != "a":
            return "You do not have authority to perform this action"
        cursor.execute(
            f"INSERT INTO Instructor (Instructor_username) VALUES ({PLACEHOLDER})",
            (request.form.get("username"), )
        )
        conn.commit()
        return redirect("/")

    cursor.execute(
        f"INSERT INTO User (Username, Password, Name, Surname, DateOfBirth) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("username"), request.form.get("password"), request.form.get("name"),
         request.form.get("surname"), request.form.get("dateOfBirth"))
    )

    instructor_usernames = [item[0] for item in cursor.execute("SELECT instructor_username FROM Instructor").fetchall()]
    if request.form.get("username") in instructor_usernames:
        user_type = "instructor"
    else:
        cursor.execute(
            f"INSERT INTO Student (Student_username) VALUES ({PLACEHOLDER})",
            (request.form.get("username"),)
        )
        user_type = "student"
    conn.commit()
    return render_template("pages/login.html", msg=f"User registered successfully as {user_type}. Please login.")

# ========================

# ========================
@app.route("/task_set_details/<set_of_task_id>", methods=["GET", "POST"])
@login_required
@instructor_only
def task_set_details(set_of_task_id):
    if request.method == "POST":
        cursor.execute(
            f"UPDATE SetOfTask SET name={PLACEHOLDER} WHERE set_of_task_id={set_of_task_id}",
            (request.form.get("taskSetName"),)
        )
        conn.commit()
        return redirect(f"/task_set_details/{set_of_task_id}")
    set_of_task = cursor.execute(f"SELECT set_of_task_id, name FROM SetOfTask WHERE Set_of_task_id='{set_of_task_id}'").fetchone()
    return render_template("pages/task_set_details.html", set_of_task=set_of_task)
# ========================


@app.route("/add_task/<set_of_task_id>", methods=["GET", "POST"])
@login_required
@instructor_only
def add_task(set_of_task_id):
    if request.method == "GET":
        return render_template("pages/add_task.html", set_of_task=set_of_task_id)
    cursor.execute(
        f"INSERT INTO Task (name,Description, task_content, Answer, set_of_task_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("taskName"), request.form.get("taskDescription"), request.form.get("taskContent"),request.form.get("taskAnswer"), set_of_task_id)
    )
    conn.commit()
    return redirect(f"/task_set_details/{set_of_task_id}")

# ========================
@app.route("/view_courses", methods=["GET"])
@login_required
@instructor_only
def view_courses():
    courses = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'").fetchall()]
    return render_template("pages/view_courses.html", courses=courses)
# ========================

# ========================
@app.route("/view_task_sets", methods=["GET"])
@login_required
@instructor_only
def view_task_sets():
    course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'").fetchall()]
    task_sets = []
    for course_code in course_codes:
        task_set = cursor.execute(f"SELECT set_of_task_id, name FROM SetOfTask WHERE course_code='{course_code}'").fetchone()
        if task_set:
            task_sets.append(task_set)
    return render_template("pages/view_task_sets.html", task_sets=task_sets)
# ========================


@app.route("/course/<course_code>")
@login_required
def course(course_code):
    if not cursor.execute(f"SELECT * FROM StudentCourseTable WHERE student_username='{session['latte_user']}' AND course_code='{course_code}'").fetchone():
        return "You do not have permission to view this page"
    task_sets = cursor.execute(f"SELECT Set_of_task_id, Name FROM SetOfTask WHERE course_code='{course_code}'").fetchall()
    return render_template("./pages/students_task_sets.html", task_sets=task_sets, course_code=course_code)


@app.route("/task_set/<task_set_id>")
@login_required
def task_set(task_set_id):
    tasks = cursor.execute(f"SELECT task_id, name FROM Task WHERE set_of_task_id='{task_set_id}'").fetchall()
    return render_template("./pages/task_sets_task.html", tasks=tasks)


@app.route("/task/<task_id>")
@login_required
def task(task_id):
    if "calibrated" not in session:
        return render_template("calibration.html", task_id=task_id)

    task = cursor.execute(f"SELECT name, description, task_content FROM Task WHERE task_id={task_id}").fetchone()

    html_formatter = HtmlFormatter(style='default')
    image_formatter = ImageFormatter(
        style='default',  # You can experiment with styles like 'monokai' or 'friendly'
        linenos=False,  # Disable line numbers
        background_color="#ffffff",  # Set a solid background color (white)
        font_size=12,  # Optional: adjust font size
        line_height=1.2  # Optional: Adjust line height if necessary
    )
    task_content = highlight(task[2], LEXER, html_formatter)
    image_content = highlight(task[2], LEXER, image_formatter)

    with open("image.png", "wb") as image_file:
        image_file.write(image_content)

    return render_template("./pages/task.html", task=task, task_content=task_content, additional_styles=html_formatter.get_style_defs())


@app.route("/generate_heatmap/<student_username>/<task_id>/<time>")
@login_required
@instructor_only
def generate_heatmap(student_username, task_id, time):
    image = Image.open("image.png")
    width = image.width
    height = image.height

    time = time.replace("+", " ").replace("-", "/")

    left_and_top = cursor.execute(f"SELECT left, top FROM TaskDimensions WHERE student_username='{student_username}' AND task_id={task_id} AND time='{time}'").fetchone()
    top = float(left_and_top[1])
    left = float(left_and_top[0])

    heatmap = np.zeros((height, width))

    record_ids = [item[0] for item in cursor.execute(f"SELECT id FROM Record WHERE task_id={task_id} AND student_username='{student_username}'").fetchall()]
    gaze_points = []
    for id in record_ids:
        gaze_points.extend(cursor.execute(f"SELECT Gaze_X,Gaze_Y FROM Fixation WHERE Record_id={id}").fetchall())

    # x: 135.29, y: 226.78
    with open("gaze_points.txt", "w") as file:
        for x, y in gaze_points:
            file.write(f"x: {x}, y: {y}\n")

    with open("gaze_points.txt") as file:
        content = file.readlines()
        coordinates = []
        for line in content:
            coordinates.append(
                (
                    float(line.split(":")[1].split(",")[0]),
                    float(line.split(":")[2])
                )
            )

    for x, y in coordinates:
        if 0 <= x-left < width and 0 <= y-top < height:  # Ensure points are within bounds
            heatmap[int(y - top), int(x - left)] += 1

    smoothed_heatmap = gaussian_filter(heatmap, sigma=15)
    smoothed_heatmap_normalized = smoothed_heatmap / smoothed_heatmap.max()

    image = Image.open("image.png").convert("RGBA")
    image = image.resize((width, height))  # Ensure the image matches dimensions

    # Create a colormap overlay
    colormap = plt.cm.jet(smoothed_heatmap_normalized)  # Apply a color map (e.g., "jet")
    colormap = (colormap[:, :, :3] * 255).astype(np.uint8)  # Convert to RGB

    # Combine heatmap with the image
    overlay = Image.fromarray(colormap).convert("RGBA")
    blended = Image.blend(image, overlay, alpha=0.5)  # Adjust alpha for transparency

    # Save and display the result
    blended.save("./static/media/heatmap.png")
    blended.show()

    return "Report saved as heatmap.png"

@app.route("/logout")
@login_required
def logout():
    session.pop("latte_user")
    session.pop("user_type")
    return redirect("/")

# ROUTES FOR PROCESSING DATA WITH AJAX

# For now, /store is the only one method in the website used with AJAX
# in order to store the gaze into the database.
# It receives a list of 20 dictionaries, and stores the received data
# into Record->Fixation table inside Latte database.
# ========================


@app.route("/add_calibration_success", methods=["POST"])
@login_required
def add_calibration_success():
    session["calibrated"] = True
    return "200"

@app.route("/store", methods=["POST"])
@login_required
def store():
    now = datetime.datetime.now()
    now = now.strftime("%H:%M:%S.%f")[:-3] + " " + now.strftime("%d/%m/%Y")

    if request.json[0] == "dim":
        cursor.execute(
            f"INSERT INTO TaskDimensions (left, top, task_id, student_username, time) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
            (request.json[1], request.json[2], int(request.json[3]), session["latte_user"], now)
        )
        conn.commit()
        return "200"
    
    cursor.execute(
        f"INSERT INTO Record (Student_username, Task_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
        (session["latte_user"], int(request.json[0]['task_id']))
    )
    # cursor.execute("SELECT LAST_INSERT_ID()")
    # id = cursor.fetchone()[0]
    id = cursor.lastrowid
    for dictionary in request.json:
        cursor.execute(
            f"INSERT INTO Fixation (Gaze_X, Gaze_Y, Gaze_Time, Record_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER},{PLACEHOLDER},{PLACEHOLDER})",
            (dictionary['x'], dictionary['y'], f"{dictionary['t']} {now.split()[1]}", id)
        )
    conn.commit()
    return "200"
# ========================


if __name__ == "__main__":
    app.run(debug=True)
