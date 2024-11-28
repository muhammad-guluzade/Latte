-- The User is an abstract Table used to create either Instructor or Student
-- It uses the ID as a primary key
CREATE TABLE User (
    ID VARCHAR(255) PRIMARY KEY,       -- Changed ID to the primary key
    Username VARCHAR(255) NOT NULL,   -- Ensure Username is NOT NULL
    Password VARCHAR(255) NOT NULL,   -- Ensure Password is NOT NULL
    Name VARCHAR(100),
    Surname VARCHAR(100),
    DateOfBirth DATE
);

-- Instructor is related to the User via Instructor_id
CREATE TABLE Instructor (
    Instructor_id VARCHAR(255) PRIMARY KEY, -- Changed Instructor_email to Instructor_id
    FOREIGN KEY (Instructor_id) REFERENCES User(ID) ON DELETE CASCADE
);

-- Course uses course code as a primary key.
-- Course codes are like the ones in our univeristy: CNG445 for example
--
-- There is one instructor per course, so we store only one instructor_id
CREATE TABLE Course (
    Course_code VARCHAR(20) PRIMARY KEY, -- Added Course Code
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Instructor_id VARCHAR(255), -- Added this field because there is one instructor for each course
    FOREIGN KEY (Instructor_id) REFERENCES Instructor(Instructor_id) ON DELETE SET NULL
);

-- Set of task has its own id that is automatically incremented when
-- adding a new set of task.
--
-- Each set of task can belong to only one course, so we store one
-- course code value
CREATE TABLE SetOfTask (
    Set_of_task_id INT AUTO_INCREMENT PRIMARY KEY, -- Added id to set of tasks
    Name VARCHAR(255) NOT NULL,
    Course_code VARCHAR(20), -- Each of set of tasks will have one course
    FOREIGN KEY (Course_code) REFERENCES Course(Course_code) ON DELETE CASCADE
);

-- Task has its own id that auto increments itself when adding a new task
-- Each task can belong to only one set of task, so we store only one 
-- set_of_task_id
CREATE TABLE Task (
    Task_id INT AUTO_INCREMENT PRIMARY KEY, -- Added id to tasks
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Answer VARCHAR(255),
    Set_of_task_id INT, -- Each task will be related to one set of tasks
    FOREIGN KEY (Set_of_task_id) REFERENCES SetOfTask(Set_of_task_id) ON DELETE CASCADE
);

-- Student is related to the User via Student_id
CREATE TABLE Student (
    Student_id VARCHAR(255) PRIMARY KEY, -- Changed Student_email to Student_id
    FOREIGN KEY (Student_id) REFERENCES User(ID) ON DELETE CASCADE
);

-- Each record will have its own id
-- The record keeps track of students solving particular tasks
CREATE TABLE Record (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Student_id VARCHAR(255),
    Task_id INT,
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE,
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
    Student_id VARCHAR(255),
    Course_code VARCHAR(20),
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE,
    FOREIGN KEY (Course_code) REFERENCES Course(Course_code) ON DELETE CASCADE,
    PRIMARY KEY (Student_id, Course_code)
);
