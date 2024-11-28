-- Step 1: Create User table (as it's referenced by Student and Instructor)
CREATE TABLE User (
    ID VARCHAR(255) PRIMARY KEY,       -- Changed ID to the primary key
    Username VARCHAR(255) NOT NULL,   -- Ensure Username is NOT NULL
    Password VARCHAR(255) NOT NULL,   -- Ensure Password is NOT NULL
    Name VARCHAR(100),
    Surname VARCHAR(100),
    DateOfBirth DATE
);

-- Step 2: Create Instructor table (depends on User table)
CREATE TABLE Instructor (
    Instructor_id VARCHAR(255) PRIMARY KEY, -- Changed Instructor_email to Instructor_id
    FOREIGN KEY (Instructor_id) REFERENCES User(ID) ON DELETE CASCADE
);

-- Step 3: Create Course table (Instructor is referenced here)
CREATE TABLE Course (
    Course_code VARCHAR(20) PRIMARY KEY, -- Added Course Code (like CNG491 or CNG300)
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Instructor_id VARCHAR(255), -- Added this field because there is one instructor for each course
    FOREIGN KEY (Instructor_id) REFERENCES Instructor(Instructor_id) ON DELETE SET NULL
);

-- Step 4: Create SetOfTask table (depends on Course table)
CREATE TABLE SetOfTask (
    Set_of_task_id INT AUTO_INCREMENT PRIMARY KEY, -- Added id to set of tasks
    Name VARCHAR(255) NOT NULL,
    Course_code VARCHAR(20), -- Each of set of tasks will have one course
    FOREIGN KEY (Course_code) REFERENCES Course(Course_code) ON DELETE CASCADE
);

-- Step 5: Create Task table (depends on SetOfTask table)
CREATE TABLE Task (
    Task_id INT AUTO_INCREMENT PRIMARY KEY, -- Added id to tasks
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Answer VARCHAR(255),
    Set_of_task_id INT, -- Each task will be related to one set of tasks
    FOREIGN KEY (Set_of_task_id) REFERENCES SetOfTask(Set_of_task_id) ON DELETE CASCADE
);

-- Step 6: Create Student table (depends on User table)
CREATE TABLE Student (
    Student_id VARCHAR(255) PRIMARY KEY, -- Changed Student_email to Student_id
    FOREIGN KEY (Student_id) REFERENCES User(ID) ON DELETE CASCADE
);

-- Step 7: Create Record table (depends on Student and Task tables)
CREATE TABLE Record (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Student_id VARCHAR(255),
    Task_id INT,
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE,
    FOREIGN KEY (Task_id) REFERENCES Task(Task_id) ON DELETE CASCADE
);

-- Step 8: Create Fixation table (depends on Record table)
CREATE TABLE Fixation (
    Gaze_X FLOAT,
    Gaze_Y FLOAT,
    Gaze_Time VARCHAR(50),
    Record_id INT,
    FOREIGN KEY (Record_id) REFERENCES Record(Id) ON DELETE CASCADE,
    PRIMARY KEY (Record_id, Gaze_Time)
);

-- Step 9: Create StudentCourseTable table (depends on Student and Course tables)
CREATE TABLE StudentCourseTable (
    Student_id VARCHAR(255),
    Course_code VARCHAR(20),
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id) ON DELETE CASCADE,
    FOREIGN KEY (Course_code) REFERENCES Course(Course_code) ON DELETE CASCADE,
    PRIMARY KEY (Student_id, Course_code)
);
