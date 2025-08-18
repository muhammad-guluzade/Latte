# Latte

## Foreword
One of the most impactful and challenging academic requirements of our university is graduation project. Having completed multiple challenging engineering and computer science courses, having done 2 internships in our fields, in our 4th year, we were able to implement our skills and expertise in one of the most exciting and significant projects - our graduation project. With the help of our brilliant supervisor, with a lot of effort, patience, and coordinated teamwork, we were able to build something truly innovative and useful in the field of Computer Engineering. We are now happy to share this work with the world and demonstrate the result of 2 semesters' hard work.

## Description
Latte is a complete ready-to-use product. Its main purpose is to help instructors analyze students' behavior while students solve various programming tasks. However, it does not use traditional methods (e.g. checking whether the answer is correct or not), it uses **eye tracking**. With students' consent, Latte uses web camera to track and analyze eye movements while they solve tasks. It collects data representing students' gaze points in a 2-dimensional array (screen pixels). Regardless of the screen size, it accurately measures each point the student looked at, and this data is then used by instructors to generate 2 types of reports: Heatmap and Gaze Plot.

### Heatmap
This report clearly shows areas at which the students looked at the most and the least. This report is useful if an instructor wants a quick and easy-to-understand report that shows where the students focus most while solving particular task.

### Gaze Plot
This is more advanced than the Heatmap, as it shows each of the gaze points in the order that they were recorded. It looks more complicated than the Heatmap, but it is more useful in terms of understanding the thought process of a student solving a task, as it shows the labeled sequence of gaze points (1-infinity).

### CSV import-export (managing the database)
Latte allows the instructors to import and export csv files that contain the data related to the gaze points. This is done to ensure that the database of our app is not very crowded with bulks of data. Once the instructor wants to regenerate some report, they can upload the csv file that they saved before, and the reports will be generated as if the data was taken from the database itself.

### Instructor functionalities
Apart from the abovementioned functionalities, Latte also allows the user to be registered as instructor with the username they received via email from the admin. If they are registrered as an instructor, they can add course, add programming tasks and task sets to that course, and edit any of that later. They can also add the students to the course so that the students can access that course's tasks. 

### Student functionalities
The students can access the programming tasks of the course they have been assigned to and solve them, entering their answer once they are done with the task.

### Formalities
Upon registering to the website, every user gives the consent to use their web cameras to collect data to analyze the gaze points.

## Tools
- The website is built using **Flask**, **HTML/CSS/JS**, and **MySQL**. 
- **Webgazer** library was used in order to track users' eye movements. 
- **Postman** was used for unit and API testing. 
- **Pytest** and **unittest** was used for testing the functions inside of the source code. 
- **Microsoft Word** was used to document our progress throughout the year. 
- **Github** was used for collaborative work and source code share.
- **Trello** was used to track the upcoming, ongoing, and completed tasks and coordinate the work within our team.
