
# Imports
# =================
from functools import wraps
from flask import Flask, render_template, request, redirect, session, flash
# from database import cursor, db
import datetime
from jinja2 import Environment
from pygments import highlight
from pygments.formatters import HtmlFormatter, ImageFormatter
from pygments.lexers import CLexer, JavaLexer, PythonLexer
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import filters
from scipy.cluster.hierarchy import linkage, fcluster
import random
# =================

# !
# CHANGE TO MYSQL AFTER
# =========================
import sqlite3
conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()
# =========================

# Creating an app that runs the entire localhost server
# =================
app = Flask(__name__)
app.secret_key = "123"
# =================

# PLACEHOLDER value makes it easy to change between sqlite3 and mysql databases
# by just changing the PLACEHOLDER to '?' for sqlite3 and '%s' for mysql
# =================
PLACEHOLDER = "?"
# =================

# !
# Lexer is global for now
LEXER = PythonLexer()

# WRAPPER FUNCTIONS

# Wrapper function that ensures that the users who are not logged in
# don't get access via entering the domains manually
# =================
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "latte_user" not in session:
            return redirect("/")
        return func(*args, **kwargs)
    return decorated_function
# =================


# Wrapper function that ensures that the users who are not logged in
# as instructors don't get access to the website_pages that were designed for
# the instructors only
# =================
def instructor_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_type" not in session:
            return redirect("/")
        if session["user_type"] != "i":
            return redirect("/")
        return func(*args, **kwargs)
    return decorated_function
# =================


# Wrapper function that ensures that the users who are not logged in
# as instructors don't get access to the website_pages that were designed for
# the instructors only
# =================
def catch_sql_error(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            flash("Sql error occured")
            return redirect("/")
    return decorated_function
# =================


# GET AND POST ROUTES

# /
# Ensures that the user of the website gets the correct html page
# based on the type and whether they are logged in.
# ========================
@app.route("/", methods=["GET"])

def index():
    if "latte_user" not in session:
        return render_template("website_pages/login.html")
    if session['user_type'] == "a":
        return render_template("website_pages/admin_panel.html")
    if session['user_type'] == "i":
        return render_template("website_pages/dashboardi.html")
    else:
        course_codes_for_student = [item[0] for item in cursor.execute(f"SELECT course_code FROM StudentCourseTable WHERE student_username='{session['latte_user']}'").fetchall()]
        return render_template("website_pages/dashboards.html", courses=course_codes_for_student)
# ========================

# /add_students_to_course
# The url that allows instructor to add single or multiple students
# to the specific course.
# ========================
@app.route("/add_students_to_course", methods=["GET", "POST"])
@login_required
@instructor_only

def add_students_to_course():
    # GET request just shows the students registered in the system and courses of the instructor
    if request.method == "GET":
        courses = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE Instructor_username='{session['latte_user']}'").fetchall()]
        students = [item[0] for item in cursor.execute("SELECT student_username FROM Student").fetchall()]
        return render_template("website_pages/add_students_to_course.html", courses=courses, students=students)

    # POST request connects one or more students to the specific course
    if request.form.get("addStudentType") == "single":
        # If the student is already enrolled in the course, notifies the instructor
        if cursor.execute(f"SELECT student_username, course_code FROM StudentCourseTable WHERE student_username='{request.form.get('singleStudent')}' AND course_code='{request.form.get('courseSelect')}'").fetchone():
            flash("Student already added to this course")
            return redirect("/add_students_to_course")
        cursor.execute(
            "INSERT INTO StudentCourseTable (student_username, course_code) VALUES (?, ?)",
            (request.form.get("singleStudent"), request.form.get("courseSelect")),
        )
        flash("Successfully added the student")
    else:
        # Creating a list of students that were chosen by the instructor
        selected_students = [value for key, value in request.form.items() if "groupStudent" in key]
        for student in selected_students:
            # If one of the students is already enrolled in the course, notifies the instructor
            if cursor.execute(
                f"SELECT student_username, course_code FROM StudentCourseTable WHERE student_username='{student}' AND course_code='{request.form.get('courseSelect')}'").fetchone():
                flash("One of the students already added to this course")
                return redirect("/add_students_to_course")
            cursor.execute(
                "INSERT INTO StudentCourseTable (student_username, course_code) VALUES (?, ?)",
                (student, request.form.get("courseSelect")),
            )
        flash("Successfully added the students")
    conn.commit()
    return redirect("/add_students_to_course")
# ========================

# /course_details/<course_code>
# Shows the details of the course related to specific instructor as well as
# allows the instructor to change name or description of the course or add
# new task set to the course.
# ========================
@app.route("/course_details/<course_code>", methods=["GET", "POST"])
@login_required
@instructor_only

def course_details(course_code):
    # GET request shows the courses related to the instructor
    if request.method == "GET":
        course = cursor.execute(f"SELECT name, description, course_code FROM Course WHERE course_code='{course_code}'").fetchone()
        return render_template("website_pages/course_details.html", course=course)

    # POST request updates the name and description of the course
    cursor.execute(
        f"UPDATE Course SET Name={PLACEHOLDER}, Description={PLACEHOLDER} WHERE course_code='{course_code}'",
        (request.form.get("courseName"), request.form.get("courseDescription"))
    )
    conn.commit()

    flash("Course updated successfully")

    return redirect("/view_courses")
# ========================

# /create_course
# Allows the instructor to create the course. Along with creating a new course,
# the instructor can create one task set and add one or multiple students to the course.
# ========================
@app.route("/create_course", methods=["GET", "POST"])
@login_required
@instructor_only

def create_course():
    # GET request displays the page with the form for creating a new course and available students to
    # enroll in the new course
    if request.method == "GET":
        students = [item[0] for item in cursor.execute(f"SELECT student_username FROM Student").fetchall()]
        return render_template("website_pages/create_course.html", students=students)

    # POST request creates a new course
    cursor.execute(
        f"INSERT INTO Course (Course_code, Name, Description, Instructor_username) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("courseCode"), request.form.get("courseName"), request.form.get("courseDescription"), session['latte_user'])
    )

    # If the instructor chose to create a task set as well
    if request.form.get("addTaskSet"):
        if request.form.get("taskSetName") == "":
            cursor.execute(f"DELETE FROM Course WHERE course_code='{request.form.get('courseCode')}'")
            flash("Please enter task set name")
            return redirect("/create_course")
        cursor.execute(
            f"INSERT INTO SetOfTask (Name, Course_code) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
            (request.form.get("taskSetName"), request.form.get("courseCode"))
        )

    # If the instructor chose to add one or more students as well
    if request.form.get("addStudents"):
        if request.form.get("studentType") == "single":
            if request.form.get("singleStudent") == "":
                cursor.execute(f"DELETE FROM Course WHERE course_code='{request.form.get('courseCode')}'")
                flash("Please select the students to add")
                return redirect("/create_course")
            cursor.execute(
                "INSERT INTO StudentCourseTable (student_username, course_code) VALUES (?, ?)",
                (request.form.get("singleStudent"), request.form.get("courseCode")),
            )
        else:
            selected_students = [value for key, value in request.form.items() if "groupStudent" in key]
            if not selected_students:
                cursor.execute(f"DELETE FROM Course WHERE course_code='{request.form.get('courseCode')}'")
                flash("Please select the students to add")
                return redirect("/create_course")
            for student in selected_students:
                cursor.execute(
                    "INSERT INTO StudentCourseTable (student_username, course_code) VALUES (?, ?)",
                    (student, request.form.get("courseCode"))
                )


    conn.commit()

    flash("Course created successfully")

    return redirect("/create_course")

# ========================


# /generate_report
# Displays the page to select the type of the report and students to generate report for
# ========================
@app.route("/generate_report", methods=["GET"])
@login_required
@instructor_only

def generate_report():
    # GET request displays the form with individual/group selection and the students related to a particular instructor
    if request.method == "GET":
        course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'")]
        students = []
        for course_code in course_codes:
            students.extend([item[0] for item in cursor.execute(f"SELECT student_username FROM StudentCourseTable WHERE course_code='{course_code}'").fetchall()])
        return render_template("website_pages/generate_report.html", students=students)
# ========================

# /login
# This is the only route that can set the user as logged in, because after signing up, the
# user has to log in with the entered credentials.
# Logs the user in as an admin, instructor, or student.
# ========================
@app.route("/login", methods=["GET", "POST"])

def login():
    # If the user is already logged in, redirect them to the main page
    if "latte_user" in session:
        return redirect("/")

    # GET request displays the login form
    if request.method == "GET":
        return render_template("website_pages/login.html")

    # POST request validates entered credentials
    password = cursor.execute(f"SELECT password FROM User WHERE username='{request.form.get('username')}'").fetchone()

    # If the password was not found for the given username, it means the user does not exist
    if not password:
        flash("The user does not exist")
        return render_template("website_pages/login.html")

    # If the password is not correct
    if password[0] != request.form.get("password"):
        flash("Passwords do not match")
        return render_template("website_pages/login.html")

    # Selecting the admin and instructor usernames to check the type of the user
    admins_usernames = [item[0] for item in cursor.execute("SELECT admin_username FROM Admin").fetchall()]
    instructors_usernames = [item[0] for item in cursor.execute("SELECT instructor_username FROM Instructor").fetchall()]

    # Setting the type of the user
    if request.form.get("username") in admins_usernames:
        session["user_type"] = "a"
    elif request.form.get("username") in instructors_usernames:
        session["user_type"] = "i"
    else:
        session["user_type"] = "s"

    # Setting the username in session to be used elsewhere in the code
    session["latte_user"] = f"{request.form.get('username')}"

    return redirect("/")
# ========================


# /signup
# Signs the new user as a student or instructor.
# This route also serves as a method for admin to add the new instructor to the database
# ========================
@app.route("/signup", methods=["GET", "POST"])

def signup():
    # If the request was issued by admin to add new instructor
    if request.args.get("admin") == "true":
        # If the user other than admin tries to access this route
        if session['user_type'] != "a":
            flash("You do not have the authority to perform this action")
            return redirect("/")
        username = cursor.execute(f"SELECT username FROM User WHERE username='{request.form.get('username')}'").fetchone()
        if username:
            flash("This username already exists")
            return redirect("/")
        cursor.execute(
            f"INSERT INTO Instructor (Instructor_username) VALUES ({PLACEHOLDER})",
            (request.form.get("username"), )
        )
        conn.commit()
        flash("Instructor username added successfully")
        return redirect("/")

    # If the user is already logged in, redirect them to the main page
    if "latte_user" in session:
        return redirect("/")

    # GET request shows the signup form
    if request.method == "GET":
        return render_template("website_pages/signup.html")

    # POST request adds the new user
    cursor.execute(
        f"INSERT INTO User (Username, Password, Name, Surname, DateOfBirth) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("username"), request.form.get("password"), request.form.get("name"),
         request.form.get("surname"), request.form.get("dateofbirth"))
    )

    # Checks whether the new user is instructor or student
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
    flash(f"User registered successfully as {user_type}. Please login.")
    return render_template("website_pages/login.html")

# ========================


# /task_set_details/<set_of_task_id>
# Shows the details of the set of tasks related to the specific instructor and allows
# the instructors to modify them or add new tasks
# ========================
@app.route("/task_set_details/<set_of_task_id>", methods=["GET", "POST"])
@login_required
@instructor_only

def task_set_details(set_of_task_id):
    # GET request shows the set of task name and tasks related to this set of task
    if request.method == "GET":
        set_of_task = cursor.execute(f"SELECT set_of_task_id, name FROM SetOfTask WHERE Set_of_task_id='{set_of_task_id}'").fetchone()
        tasks = cursor.execute(f"SELECT task_id, name FROM Task WHERE set_of_task_id={set_of_task_id}").fetchall()
        return render_template("website_pages/task_set_details.html", set_of_task=set_of_task, tasks=tasks)

    # POST request updates the name of the set of task
    cursor.execute(
        f"UPDATE SetOfTask SET name={PLACEHOLDER} WHERE set_of_task_id={set_of_task_id}",
        (request.form.get("taskSetName"),)
    )
    conn.commit()

    flash("Task set name updated successfully")

    return redirect(f"/task_set_details/{set_of_task_id}")
# ========================


# /task_details/<task_id>
# Shows the task details (name, description, content, and answer) and allows the instructor
# to modify them
# ========================
@app.route("/task_details/<task_id>", methods=["GET", "POST"])
@login_required
@instructor_only

def task_details(task_id):
    # GET request shows the task with its details
    if request.method == "GET":
        task = cursor.execute(f"SELECT name, description, task_content, answer FROM Task WHERE task_id={task_id}").fetchone()
        return render_template("./website_pages/task_details.html", task=task, task_id=task_id)

    # POST request updates the details of the task
    cursor.execute(
        f"UPDATE Task SET Name={PLACEHOLDER}, Description={PLACEHOLDER}, Task_content={PLACEHOLDER}, Answer={PLACEHOLDER} WHERE task_id={task_id}",
        (request.form.get("taskName"), request.form.get("taskDescription"), request.form.get("taskContent"), request.form.get("taskAnswer"))
    )
    conn.commit()

    flash("Task updated successfully")

    return redirect(f"/task_details/{task_id}")
# ========================


# /add_task/<set_of_task_id>
# Allows the instructor to add task for the specific set of task
# ========================
@app.route("/add_task/<set_of_task_id>", methods=["GET", "POST"])
@login_required
@instructor_only

def add_task(set_of_task_id):
    # GET request displays the form to add new task
    if request.method == "GET":
        return render_template("website_pages/add_task.html", set_of_task=set_of_task_id)

    # POST request adds a new task to the set of task
    cursor.execute(
        f"INSERT INTO Task (name,Description, task_content, Answer, set_of_task_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("taskName"), request.form.get("taskDescription"), request.form.get("taskContent"),request.form.get("taskAnswer"), set_of_task_id)
    )
    conn.commit()
    return redirect(f"/task_set_details/{set_of_task_id}")
# ========================


# /add_task_set/<course_code>
# Adds set of task to a specific course
# ========================
@app.route("/add_task_set/<course_code>", methods=["GET", "POST"])
@login_required
@instructor_only

def add_task_set(course_code):
    # GET request displays the form to add new set of task
    if request.method == "GET":
        return render_template("./website_pages/add_task_set.html", course_code=course_code)

    # POST request adds new set of task
    cursor.execute(
        f"INSERT INTO SetOfTask (name, course_code) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
        (request.form.get("taskSetName"), course_code)
    )
    conn.commit()

    flash("Task set added successfully")

    return redirect(f"/course_details/{course_code}")
# ========================


# /view_courses
# Allows the instructor to view the courses that they give
# ========================
@app.route("/view_courses", methods=["GET"])
@login_required
@instructor_only

def view_courses():
    courses = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'").fetchall()]
    return render_template("website_pages/view_courses.html", courses=courses)
# ========================


# /view_task_sets
# # Allows the instructor to view sets of tasks that they created
# ========================
@app.route("/view_task_sets", methods=["GET"])
@login_required
@instructor_only

def view_task_sets():
    course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'").fetchall()]
    print(course_codes)
    task_sets = []
    for course_code in course_codes:
        task_sets = cursor.execute(f"SELECT set_of_task_id, name FROM SetOfTask WHERE course_code='{course_code}'").fetchall()
    return render_template("website_pages/view_task_sets.html", task_sets=task_sets)
# ========================


# /course/<course_code>
# Allows the student to see the courses they are registered in
# ========================
@app.route("/course/<course_code>")
@login_required

def course(course_code):
    # If another student tries to view the course contents they are not registered in
    if not cursor.execute(f"SELECT * FROM StudentCourseTable WHERE student_username='{session['latte_user']}' AND course_code='{course_code}'").fetchone():
        flash("You do not have permission to view this page")
        return redirect(f"/course/{course_code}")
    task_sets = cursor.execute(f"SELECT Set_of_task_id, Name FROM SetOfTask WHERE course_code='{course_code}'").fetchall()
    return render_template("./website_pages/students_task_sets.html", task_sets=task_sets, course_code=course_code)
# ========================


# /task_set/<task_set_id>
# Allows the student to view the specific task set contents (tasks)
# ========================
@app.route("/task_set/<task_set_id>")
@login_required
def task_set(task_set_id):
    tasks = cursor.execute(f"SELECT task_id, name FROM Task WHERE set_of_task_id='{task_set_id}'").fetchall()
    completed_tasks = []

    for task_id, name in tasks:
        completed_tasks.append((task_id, name, cursor.execute(f"SELECT task_id FROM TaskDimensions WHERE student_username='{session['latte_user']}'").fetchone() != None))

    return render_template("./website_pages/task_sets_task.html", tasks=completed_tasks)
# ========================


# /task/<task_id>
# Allows the student to complete the task while their gaze points are being recorded
# ========================
@app.route("/task/<task_id>")
@login_required

def task(task_id):
    # If the student did not complete the calibration
    if "calibrated" not in session:
        return render_template("calibration.html", task_id=task_id)

    # Selecting the task from the database
    task = cursor.execute(f"SELECT name, description, task_content FROM Task WHERE task_id={task_id}").fetchone()

    # Saving the task as an image of highlighted code to later be formatted as a heatmap
    image_formatter = ImageFormatter(
        style='default',
        linenos=False,
        background_color="#ffffff",
        font_size=12,
        line_height=1.2
    )
    image_content = highlight(task[2], LEXER, image_formatter)

    with open("./static/media/image.png", "wb") as image_file:
        image_file.write(image_content)

    # Formatting the task content as a highlighted code to be displayed as text on
    # the html page
    html_formatter = HtmlFormatter(style='default')
    task_content = highlight(task[2], LEXER, html_formatter)

    return render_template("./website_pages/task.html", task_id=task_id, task=task, task_content=task_content, additional_styles=html_formatter.get_style_defs())
# ========================


# Formats the image and adds the heatmap over it based on the calculated values (heatmap)
# and width and height of the image
# ========================
def generate_and_save_heatmap(heatmap, width, height, student_username, task_id, time=""):
    time = time.replace("/", "-").replace(":", ".")

    smoothed_heatmap = filters.gaussian(heatmap, sigma=15)
    smoothed_heatmap_normalized = smoothed_heatmap / smoothed_heatmap.max()

    image = Image.open("./static/media/image.png").convert("RGBA")
    image = image.resize((width, height))

    colormap = plt.cm.jet(smoothed_heatmap_normalized)
    colormap = (colormap[:, :, :3] * 255).astype(np.uint8)

    overlay = Image.fromarray(colormap).convert("RGBA")
    blended = Image.blend(image, overlay, alpha=0.5)

    blended.save(f"./static/media/heatmap_{student_username}_{task_id}_{time}.png")

    flash("Report generated successfully")

    return f"../../static/media/heatmap_{student_username}_{task_id}_{time}.png"
# ========================


# /generate_heatmap_individual
# Generates the heatmap for one student
# ========================
@app.route("/generate_heatmap_individual", methods=["GET", "POST"])
@login_required
@instructor_only

def generate_heatmap_individual():

    if request.method == "GET":
        return redirect("/generate_report")

    # Selecting the first instance of the student completing some task
    data = cursor.execute(f"SELECT task_id, student_username, time FROM TaskDimensions WHERE student_username='{request.form.get('individualStudent')}'").fetchone()

    # Setting up student's username, task id that they completed, and time at which they completed
    # the task. This gives us uniqueness.
    student_username = data[1]
    task_id = data[0]
    time = data[2]

    # Opening the unformatted image (without heatmap) and taking its width and height
    image = Image.open("./static/media/image.png")
    width = image.width
    height = image.height

    # Retrieving the dimensions of the screen of the student who was completing the task
    left_and_top = cursor.execute(f"SELECT left, top FROM TaskDimensions WHERE student_username='{student_username}' AND task_id={task_id} AND time='{time}'").fetchone()
    top = float(left_and_top[1])
    left = float(left_and_top[0])

    if request.form.get("reportFormat") == "gazeplot":
        # Load the image
        image = mpimg.imread("./static/media/image.png")
        image_height, image_width = image.shape[:2]

        users = [request.form.get('individualStudent')]
        num_users = len(users)
        colors = ["blue"]

        user_data = {}

        for user, color in zip(users, colors):
            record_ids = [item[0] for item in cursor.execute(f"SELECT id FROM Record WHERE task_id={task_id} AND student_username='{student_username}'").fetchall()]

            coordinates = []
            for id in record_ids:
                coordinates.extend(cursor.execute(f"SELECT Gaze_X, Gaze_Y, Gaze_Time FROM Fixation WHERE Record_id={id}").fetchall())

            gaze_x = np.array([])
            gaze_y = np.array([])
            raw_times = []

            for x, y, t in coordinates:
                if 0 <= x - left < width and 0 <= y - top < height:
                    gaze_x = np.append(gaze_x, x - left)
                    gaze_y = np.append(gaze_y, y - top)
                    raw_times.append(t.split()[0])
            
            timestamps = [datetime.datetime.strptime(t, "%H:%M:%S.%f") for t in raw_times]

            fixation_durations = [max(50, (timestamps[i + 1] - timestamps[i]).total_seconds() * 1000) for i in range(len(timestamps) - 1)]
            fixation_durations.append(fixation_durations[-1])

            min_size, max_size = 100, 500
            sizes = np.interp(fixation_durations, (min(fixation_durations), max(fixation_durations)), (min_size, max_size))

            user_data[user] = {"x": gaze_x, "y": gaze_y, "timestamps": timestamps, "sizes": sizes, "color": color}

        fig, ax = plt.subplots(figsize=(image_width / 100, image_height / 100), dpi=100)
        ax.set_xlim(0, image_width)
        ax.set_ylim(image_height, 0)
        ax.imshow(image, extent=[0, image_width, image_height, 0], aspect='auto')

        for user, data in user_data.items():
            ax.plot(data["x"], data["y"], color=data["color"], linestyle='-', linewidth=1, alpha=0.7)
            ax.scatter(data["x"], data["y"], color=data["color"], s=data["sizes"], edgecolors=data["color"], alpha=0.4, label=user)
            
            for i, (x, y) in enumerate(zip(data["x"], data["y"])):
                ax.text(x, y, str(i + 1), fontsize=8, ha='center', va='center', color='black')

        ax.set_title("")
        ax.set_xticks([])
        ax.set_yticks([])

        path = "./static/media/gaze_plot.png"

        plt.savefig("./static/media/gaze_plot.png", dpi=300, bbox_inches='tight', pad_inches=0)

        course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'")]
        students = []
        for course_code in course_codes:
            students.extend([item[0] for item in cursor.execute(f"SELECT student_username FROM StudentCourseTable WHERE course_code='{course_code}'").fetchall()])

        return render_template("./website_pages/generate_report.html", path=path, students=students)


    # Initializing the heatmap as a 2-dimensional table
    heatmap = np.zeros((height, width))

    # Retrieving the records related to the student
    record_ids = [item[0] for item in cursor.execute(
        f"SELECT id FROM Record WHERE task_id={task_id} AND student_username='{student_username}'").fetchall()]

    # Retrieving each gaze point of the student and saving them as a list of tuples [(x1, y1), (x2, y2), ...]
    coordinates = []
    for id in record_ids:
        coordinates.extend(cursor.execute(f"SELECT Gaze_X,Gaze_Y FROM Fixation WHERE Record_id={id}").fetchall())

    # Generating the heatmap based on the width and height of the image and coordinates
    # of the gaze points
    for x, y in coordinates:
        if 0 <= x - left < width and 0 <= y - top < height:
            heatmap[int(y - top), int(x - left)] += 1

    # Saving the heatmap
    path = generate_and_save_heatmap(heatmap, width, height, student_username, task_id, time)

    course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'")]
    students = []
    for course_code in course_codes:
        students.extend([item[0] for item in cursor.execute(f"SELECT student_username FROM StudentCourseTable WHERE course_code='{course_code}'").fetchall()])

    return render_template("./website_pages/generate_report.html", path=path, students=students)
# ========================


# /generate_heatmap_group
# Generates the heatmap for multiple students
# ========================
@app.route("/generate_heatmap_group", methods=["GET", "POST"])
@login_required
@instructor_only

def generate_heatmap_group():

    if request.method == "GET":
        return redirect("/generate_report")

    # Creating the list of students that were chosen by the instructor
    selected_students = [value for key, value in request.form.items() if "groupStudent" in key]

    # Opening the unformatted image (without heatmap) and taking its width and height
    image = Image.open("./static/media/image.png")
    width = image.width
    height = image.height

    # Initializing the heatmap as a 2-dimensional table
    heatmap = np.zeros((height, width))

    student_usernames = ""
    task_id = None

    if request.form.get("reportFormat") == "gazeplot":
        image = mpimg.imread("./static/media/image.png")
        image_height, image_width = image.shape[:2]

        users = [value for key, value in request.form.items() if "groupStudent" in key]
        colors = [f'#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}' for _ in range(len(users))]
        
        user_data = {}

        for user, color in zip(users, colors):

            # Selecting the first instance of the student completing some task
            data = cursor.execute(f"SELECT task_id, student_username, time FROM TaskDimensions WHERE student_username='{user}'").fetchone()

            # Setting up student's username, task id that they completed, and time at which they completed
            # the task. This gives us uniqueness.
            student_username = data[1]
            task_id = data[0]
            time = data[2]

            student_usernames += f"{student_username}_"

            # Retrieving the dimensions of the screen of the student who was completing the task
            left_and_top = cursor.execute(f"SELECT left, top FROM TaskDimensions WHERE student_username='{student_username}' AND task_id={task_id} AND time='{time}'").fetchone()
            top = float(left_and_top[1])
            left = float(left_and_top[0])

            record_ids = [item[0] for item in cursor.execute(f"SELECT id FROM Record WHERE task_id={task_id} AND student_username='{user}'").fetchall()]

            coordinates = []
            for id in record_ids:
                coordinates.extend(cursor.execute(f"SELECT Gaze_X, Gaze_Y, Gaze_Time FROM Fixation WHERE Record_id={id}").fetchall())

            gaze_x = np.array([])
            gaze_y = np.array([])
            raw_times = []

            for x, y, t in coordinates:
                if 0 <= x - left < width and 0 <= y - top < height:
                    gaze_x = np.append(gaze_x, x - left)
                    gaze_y = np.append(gaze_y, y - top)
                    raw_times.append(t.split()[0])
            
            timestamps = [datetime.datetime.strptime(t, "%H:%M:%S.%f") for t in raw_times]

            fixation_durations = [max(50, (timestamps[i + 1] - timestamps[i]).total_seconds() * 1000) for i in range(len(timestamps) - 1)]
            fixation_durations.append(fixation_durations[-1])

            min_size, max_size = 100, 500
            sizes = np.interp(fixation_durations, (min(fixation_durations), max(fixation_durations)), (min_size, max_size))

            user_data[user] = {"x": gaze_x, "y": gaze_y, "timestamps": timestamps, "sizes": sizes, "color": color}

        fig, ax = plt.subplots(figsize=(image_width / 100 + 3, image_height / 100), dpi=100)  # Add extra width for legend
        ax.set_xlim(0, image_width)
        ax.set_ylim(image_height, 0)
        ax.imshow(image, extent=[0, image_width, image_height, 0], aspect='auto')

        for user, data in user_data.items():
            ax.plot(data["x"], data["y"], color=data["color"], linestyle='-', linewidth=1, alpha=0.7)
            ax.scatter(data["x"], data["y"], color=data["color"], s=data["sizes"], edgecolors=data["color"], alpha=0.4, label=user)
            
            for i, (x, y) in enumerate(zip(data["x"], data["y"])):
                ax.text(x, y, str(i + 1), fontsize=8, ha='center', va='center', color='black')

        ax.set_title("")
        ax.set_xticks([])
        ax.set_yticks([])

        # Adjust layout to make space for legend
        fig.subplots_adjust(right=0.8)  # Shift the plot to the left to make space

        # Place legend outside the plot
        ax.legend(title="Users", loc="center left", bbox_to_anchor=(1, 0.5))

        path = "./static/media/gaze_plot.png"

        # Save the figure
        plt.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0)


        course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'")]
        students = []
        for course_code in course_codes:
            students.extend([item[0] for item in cursor.execute(f"SELECT student_username FROM StudentCourseTable WHERE course_code='{course_code}'").fetchall()])

        return render_template("./website_pages/generate_report.html", path=path, students=students)

    for student in selected_students:
        # Selecting the first instance of the student completing some task
        data = cursor.execute(f"SELECT task_id, student_username, time FROM TaskDimensions WHERE student_username='{student}'").fetchone()

        # Setting up student's username, task id that they completed, and time at which they completed
        # the task. This gives us uniqueness.
        student_username = data[1]
        task_id = data[0]
        time = data[2]

        student_usernames += f"{student_username}_"

        # Retrieving the dimensions of the screen of the student who was completing the task
        left_and_top = cursor.execute(f"SELECT left, top FROM TaskDimensions WHERE student_username='{student_username}' AND task_id={task_id} AND time='{time}'").fetchone()
        top = float(left_and_top[1])
        left = float(left_and_top[0])

        # Retrieving the records related to the student
        record_ids = [item[0] for item in cursor.execute(
            f"SELECT id FROM Record WHERE task_id={task_id} AND student_username='{student_username}'").fetchall()]

        # Retrieving each gaze point of each student and saving them as a list of tuples [(x1, y1), (x2, y2), ...]
        coordinates = []
        for id in record_ids:
            coordinates.extend(cursor.execute(f"SELECT Gaze_X,Gaze_Y FROM Fixation WHERE Record_id={id}").fetchall())

        # Generating the heatmap based on the width and height of the image and coordinates
        # of the gaze points
        for x, y in coordinates:
            if 0 <= x - left < width and 0 <= y - top < height:
                heatmap[int(y - top), int(x - left)] += 1

    # Saving the heatmap
    path = generate_and_save_heatmap(heatmap, width, height, student_usernames, task_id)

    course_codes = [item[0] for item in cursor.execute(f"SELECT course_code FROM Course WHERE instructor_username='{session['latte_user']}'")]
    students = []
    for course_code in course_codes:
        students.extend([item[0] for item in cursor.execute(f"SELECT student_username FROM StudentCourseTable WHERE course_code='{course_code}'").fetchall()])

    return render_template("./website_pages/generate_report.html", path=path, students=students)
# ========================


# /logout
# Logs the user out
# ========================
@app.route("/logout")
@login_required

def logout():
    session.pop("latte_user")
    session.pop("user_type")
    return redirect("/")
# ========================


@app.route("/save_answer/<task_id>", methods=["GET", "POST"])
@login_required
def save_answer(task_id):
    cursor.execute(f"UPDATE Task SET student_answer={PLACEHOLDER} WHERE task_id={task_id}", (request.form.get("answer"),))
    conn.commit()
    return redirect("/")


@app.route("/save_csv")
@login_required
@instructor_only
def save_csv():
    tasks_completed_by_students = set(cursor.execute("SELECT task_id, student_username FROM Record").fetchall())
    
    tasks_completed_by_students_with_task_names = []

    for task_id, student_username in tasks_completed_by_students:
        tasks_completed_by_students_with_task_names.append((task_id, student_username, cursor.execute(f"SELECT name FROM Task WHERE task_id={task_id}").fetchone()[0]))

    return render_template("./website_pages/save_csv.html", tasks_names_and_students=tasks_completed_by_students_with_task_names)


@app.route("/save_csv/<student_username>/<task_id>")
@login_required
@instructor_only
def save_csv_specific_student(student_username, task_id):
    records = [item[0] for item in cursor.execute(f"SELECT id FROM Record WHERE student_username='{student_username}' AND task_id={task_id}").fetchall()]
    fixations = []

    for record in records:
        fixations.extend(cursor.execute(f"SELECT * FROM Fixation WHERE record_id={record}").fetchall())
    
    with open(f"./static/csv/{student_username}_{task_id}.csv", "w") as file:
        string = ""
        for fixation in fixations:
            string += f"{fixation[0]},{fixation[1]},{fixation[2]},{fixation[3]}\n"
            cursor.execute(f"DELETE FROM Fixation WHERE record_id={fixation[3]} AND gaze_time='{fixation[2]}'")
        file.write(string)

    conn.commit()
    return "200"

# ROUTES FOR PROCESSING DATA WITH AJAX


# /add_calibration_success
# Send AJAX call to the server to indicate that the calibration was completed
# ========================
@app.route("/add_calibration_success", methods=["POST"])
@login_required

def add_calibration_success():
    session["calibrated"] = True
    return "200"
# ========================


# /store
# AJAX call is sent to this route to save the gazepoints while the student is completing the task
# It also serves as a route to be called when saving the dimensions of the screen of the student
# ========================
@app.route("/store", methods=["POST"])
@login_required
def store():
    # Get the current time
    now = datetime.datetime.now()
    now = now.strftime("%H:%M:%S.%f")[:-3] + " " + now.strftime("%d/%m/%Y")

    # If the call intends to save the dimensions of the screen of the student
    if request.json[0] == "dim":
        cursor.execute(
            f"INSERT INTO TaskDimensions (left, top, task_id, student_username, time) VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})",
            (request.json[1], request.json[2], int(request.json[3]), session["latte_user"], now)
        )
        conn.commit()
        return "200"

    # Creating a new record to store 20 gazepoints (One record contains 20 gazepoints)
    cursor.execute(
        f"INSERT INTO Record (Student_username, Task_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
        (session["latte_user"], int(request.json[0]['task_id']))
    )
    # cursor.execute("SELECT LAST_INSERT_ID()")
    # id = cursor.fetchone()[0]
    id = cursor.lastrowid

    gaze_data = []
    for dictionary in request.json:
        gaze_data.append([dictionary['x'], dictionary['y'], dictionary['t']])
    
    gaze_points = np.array([[row[0], row[1]] for row in gaze_data])
    gaze_times = [row[2] for row in gaze_data]

    # The bigger the threshold, the more gazepoints in one area average out to 1 gaze point
    threshold = 15
    Z = linkage(gaze_points, method='single')
    clusters = fcluster(Z, threshold, criterion='distance')

    unique_clusters = set(clusters)

    for cluster_id in unique_clusters:
        indices = [i for i, c in enumerate(clusters) if c == cluster_id]
        cluster_points = gaze_points[indices]
        
        avg_x = np.mean(cluster_points[:, 0])
        avg_y = np.mean(cluster_points[:, 1])
        min_time = min([gaze_times[i] for i in indices])

        cursor.execute(
            f"INSERT INTO Fixation (Gaze_X, Gaze_Y, Gaze_Time, Record_id) VALUES ({PLACEHOLDER}, {PLACEHOLDER},{PLACEHOLDER},{PLACEHOLDER})",
            (round(avg_x, 2), round(avg_y, 2), f"{min_time} {now.split()[1]}", id)
        )
    conn.commit()
    return "200"
# ========================


if __name__ == "__main__":
    app.run(debug=True)
