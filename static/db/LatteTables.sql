-- The User is an abstract Table used to create either Instructor or Student
-- It uses the ID as a primary key
CREATE TABLE User (
    Username VARCHAR(255) PRIMARY KEY NOT NULL,   -- Ensure Username is NOT NULL
    Password VARCHAR(255) NOT NULL,   -- Ensure Password is NOT NULL
    Name VARCHAR(100),
    Surname VARCHAR(100),
    DateOfBirth DATE
);

-- Instructor is related to the User via Instructor_id
CREATE TABLE Instructor (
    Instructor_username VARCHAR(255) PRIMARY KEY, -- Changed Instructor_email to Instructor_username
    FOREIGN KEY (Instructor_username) REFERENCES User(username) ON DELETE CASCADE
);

-- Course uses course code as a primary key.
-- Course codes are like the ones in our univeristy: CNG445 for example
--
-- There is one instructor per course, so we store only one instructor_username
CREATE TABLE Course (
    Course_code VARCHAR(20) PRIMARY KEY, -- Added Course Code
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Instructor_username VARCHAR(255), -- Added this field because there is one instructor for each course
    FOREIGN KEY (Instructor_username) REFERENCES Instructor(Instructor_username) ON DELETE SET NULL
);

-- Set of task has its own username that is automatically incremented when
-- adding a new set of task.
--
-- Each set of task can belong to only one course, so we store one
-- course code value
CREATE TABLE SetOfTask (
    Set_of_task_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Added id to set of tasks
    Name VARCHAR(255) NOT NULL,
    Course_code VARCHAR(20), -- Each of set of tasks will have one course
    FOREIGN KEY (Course_code) REFERENCES Course(Course_code) ON DELETE CASCADE
);

-- Task has its own id that auto increments itself when adding a new task
-- Each task can belong to only one set of task, so we store only one 
-- set_of_task_id
CREATE TABLE Task (
    Task_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Added id to tasks
    Pl VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Task_content TEXT,
    Answer VARCHAR(255),
    Student_answer VARCHAR(255),
    Set_of_task_id INT, -- Each task will be related to one set of tasks
    FOREIGN KEY (Set_of_task_id) REFERENCES SetOfTask(Set_of_task_id) ON DELETE CASCADE
);

CREATE TABLE TaskDimensions (
    left FLOAT,
    top FLOAT,
    task_id INTEGER,
    student_username VARCHAR(255),
    time VARCHAR(255),
    FOREIGN KEY (task_id) REFERENCES Task(task_id) ON DELETE CASCADE,
    FOREIGN KEY (student_username) REFERENCES Student(student_username) ON DELETE CASCADE,
    PRIMARY KEY(task_id, student_username, time)
);

-- Student is related to the User via Student_username
CREATE TABLE Student (
    Student_username VARCHAR(255) PRIMARY KEY, -- Changed Student_email to Student_username
    FOREIGN KEY (Student_username) REFERENCES User(username) ON DELETE CASCADE
);

-- Admin is related to the User via Admin_username
CREATE TABLE Admin (
    Admin_username VARCHAR(255) PRIMARY KEY,
    FOREIGN KEY (Admin_username) REFERENCES User(username) ON DELETE CASCADE
);

-- Each record will have its own id
-- The record keeps track of students solving particular tasks
CREATE TABLE Record (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_username VARCHAR(255),
    Task_id INT,
    FOREIGN KEY (Student_username) REFERENCES Student(Student_username) ON DELETE CASCADE,
    FOREIGN KEY (Task_id) REFERENCES Task(Task_id) ON DELETE CASCADE
);

-- Fixation contains x,y, and time of the gaze
-- 
-- Each fixation can belong to only one record, so we store only one record
-- id in this table.
CREATE TABLE Fixation (
    Gaze_X FLOAT,
    Gaze_Y FLOAT,
    Gaze_Time VARCHAR(50),
    Record_id INT,
    FOREIGN KEY (Record_id) REFERENCES Record(Id) ON DELETE CASCADE,
    PRIMARY KEY (Record_id, Gaze_Time)
);

-- This is additional table to connect students to courses, since
-- one student can be registered to multiple courses, and courses
-- can have multiple registered students.
CREATE TABLE StudentCourseTable (
    Student_username VARCHAR(255),
    Course_code VARCHAR(20),
    FOREIGN KEY (Student_username) REFERENCES Student(Student_username) ON DELETE CASCADE,
    FOREIGN KEY (Course_code) REFERENCES Course(Course_code) ON DELETE CASCADE,
    PRIMARY KEY (Student_username, Course_code)
);

CREATE TABLE TaskLines (
    Line VARCHAR(255) NOT NULL,
    Line_cor INT NOT NULL,
    task_id INT NOT NULL
)
