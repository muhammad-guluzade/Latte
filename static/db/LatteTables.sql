CREATE TABLE User (
    Email VARCHAR(255) PRIMARY KEY,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(100),
    Surname VARCHAR(100),
    DateOfBirth DATE,
	ID VARCHAR(255)
);

CREATE TABLE Student (
    Student_Email VARCHAR(255),
    FOREIGN KEY (Student_Email) REFERENCES User(Email) ON DELETE CASCADE,
    PRIMARY KEY (Student_Email)
);

CREATE TABLE Instructor (
    Instructor_Email VARCHAR(255),
    FOREIGN KEY (Instructor_Email) REFERENCES User(Email) ON DELETE CASCADE,
    PRIMARY KEY (Instructor_Email)
);

CREATE TABLE Course (
    Name VARCHAR(255) PRIMARY KEY,
    Description TEXT
);

CREATE TABLE Task (
    Name VARCHAR(255) PRIMARY KEY,
    Description TEXT,
    Answer VARCHAR(255)
);

CREATE TABLE SetOfTask (
    Name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Join_Table (
    Student_Email VARCHAR(255),
    Course_Name VARCHAR(255),
    FOREIGN KEY (Student_Email) REFERENCES Student(Student_Email) ON DELETE CASCADE,
    FOREIGN KEY (Course_Name) REFERENCES Course(Name) ON DELETE CASCADE,
    PRIMARY KEY (Student_Email, Course_Name)
);

CREATE TABLE Add_Table (
    Instructor_Email VARCHAR(255),
    Course_Name VARCHAR(255),
    FOREIGN KEY (Instructor_Email) REFERENCES Instructor(Instructor_Email) ON DELETE CASCADE,
    FOREIGN KEY (Course_Name) REFERENCES Course(Name) ON DELETE CASCADE,
    PRIMARY KEY (Instructor_Email, Course_Name)
);

CREATE TABLE Solve_Table (
    Student_Email VARCHAR(255),
    Task_Name VARCHAR(255),
    Gaze_X FLOAT,
    Gaze_Y FLOAT,
    Gaze_Time VARCHAR(50), /* HH:MM:SS.millisecond DD/MM/YYYY */
    FOREIGN KEY (Student_Email) REFERENCES Student(Student_Email) ON DELETE CASCADE,
    FOREIGN KEY (Task_Name) REFERENCES Task(Name) ON DELETE CASCADE,
    PRIMARY KEY (Student_Email, Gaze_Time) /* Changed the primary key */
);

CREATE TABLE Include_Table (
    Course_Name VARCHAR(255),
    Set_Name VARCHAR(255),
    FOREIGN KEY (Course_Name) REFERENCES Course(Name) ON DELETE CASCADE,
    FOREIGN KEY (Set_Name) REFERENCES SetOfTask(Name) ON DELETE CASCADE,
    PRIMARY KEY (Course_Name, Set_Name)
);

CREATE TABLE Has_Table (
    Set_Name VARCHAR(255),
    Task_Name VARCHAR(255),
    FOREIGN KEY (Set_Name) REFERENCES SetOfTask(Name) ON DELETE CASCADE,
    FOREIGN KEY (Task_Name) REFERENCES Task(Name) ON DELETE CASCADE,
    PRIMARY KEY (Set_Name, Task_Name)
);
