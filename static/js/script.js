//Create Course Page (create_course.html)
if (document.getElementById("courseForm")) {
    document.getElementById("addTaskSet").addEventListener("change", function () {
        document.getElementById("taskSetSection").style.display = this.checked ? "block" : "none";
    });

    document.getElementById("addTasks").addEventListener("change", function () {
        document.getElementById("tasksSection").style.display = this.checked ? "block" : "none";
    });

    document.getElementById("addStudents").addEventListener("change", function () {
        document.getElementById("studentSection").style.display = this.checked ? "block" : "none";
    });

    document.getElementById("singleStudent").addEventListener("change", function () {
        document.getElementById("singleStudentSection").style.display = this.checked ? "block" : "none";
        document.getElementById("multipleStudentsSection").style.display = "none";
    });

    document.getElementById("multipleStudents").addEventListener("change", function () {
        document.getElementById("multipleStudentsSection").style.display = this.checked ? "block" : "none";
        document.getElementById("singleStudentSection").style.display = "none";
    });

    document.getElementById("courseForm").addEventListener("submit", function (event) {
        event.preventDefault();
        document.getElementById("confirmationMessage").style.display = "block";
    });
}

//Generate Report Page (generate_report.html)
if (document.getElementById("reportForm")) {
    document.getElementById("reportType").addEventListener("change", function () {
        const individualReportSection = document.getElementById("individualReportSection");
        const groupReportSection = document.getElementById("groupReportSection");

        if (this.value === "individual") {
            individualReportSection.style.display = "block";
            groupReportSection.style.display = "none";
        } else if (this.value === "group") {
            individualReportSection.style.display = "none";
            groupReportSection.style.display = "block";
        } else {
            individualReportSection.style.display = "none";
            groupReportSection.style.display = "none";
        }
    });

    document.getElementById("reportForm").addEventListener("submit", function (event) {
        event.preventDefault();
        document.getElementById("reportConfirmationMessage").style.display = "block";
    });
}

//View Courses Page (view_courses.html)
if (document.getElementById("courseList")) {
    const courses = [
        { id: 1, name: "Course 1" },
        { id: 2, name: "Course 2" },
        { id: 3, name: "Course 3" }
    ];

    const courseList = document.getElementById("courseList");
    courses.forEach(course => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${course.name}</span>
            <a href="course_details.html?courseId=${course.id}">View Details</a>
        `;
        courseList.appendChild(listItem);
    });
}

//View Task Sets Page (view_task_sets.html)
if (document.getElementById("taskSetList")) {
    const taskSets = [
        { id: 1, name: "Task Set 1" },
        { id: 2, name: "Task Set 2" },
        { id: 3, name: "Task Set 3" }
    ];

    const taskSetList = document.getElementById("taskSetList");
    taskSets.forEach(taskSet => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${taskSet.name}</span>
            <a href="task_set_details.html?taskSetId=${taskSet.id}">View Details</a>
        `;
        taskSetList.appendChild(listItem);
    });
}

//Add Students to Course Page (add_students_to_course.html)
if (document.getElementById("addStudentsForm")) {
    document.getElementById("addSingleStudent").addEventListener("change", function () {
        document.getElementById("singleStudentSection").style.display = this.checked ? "block" : "none";
        document.getElementById("multipleStudentsSection").style.display = "none";
    });

    document.getElementById("addMultipleStudents").addEventListener("change", function () {
        document.getElementById("multipleStudentsSection").style.display = this.checked ? "block" : "none";
        document.getElementById("singleStudentSection").style.display = "none";
    });

    document.getElementById("addStudentsForm").addEventListener("submit", function (event) {
        event.preventDefault();
        document.getElementById("addStudentConfirmation").style.display = "block";
    });
}

//Function to filter students in the single or multiple student list
function filterStudents(listId, searchInputId) {
    const searchInput = document.getElementById(searchInputId).value.toLowerCase();
    const studentList = document.getElementById(listId);

    Array.from(studentList.children).forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(searchInput) ? "block" : "none";
    });
}

//Sample data for courses and task sets
const courses = [
    { id: 1, name: "Course 1", description: "Description of Course 1" },
    { id: 2, name: "Course 2", description: "Description of Course 2" },
    { id: 3, name: "Course 3", description: "Description of Course 3" }
];

const taskSets = [
    { id: 1, name: "Task Set 1", tasks: ["Task 1", "Task 2"] },
    { id: 2, name: "Task Set 2", tasks: ["Task 3", "Task 4"] },
    { id: 3, name: "Task Set 3", tasks: ["Task 5", "Task 6"] }
];

//Course Details Page
if (document.getElementById("courseDetailsForm")) {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = parseInt(urlParams.get("courseId"));
    const course = courses.find(c => c.id === courseId);

    if (course) {
        document.getElementById("courseName").value = course.name;
        document.getElementById("courseDescription").value = course.description;

        document.getElementById("courseDetailsForm").addEventListener("submit", function(event) {
            event.preventDefault();
            course.name = document.getElementById("courseName").value;
            course.description = document.getElementById("courseDescription").value;
            document.getElementById("updateConfirmation").style.display = "block";
        });
    }
}

//Task Set Details Page
if (document.getElementById("taskSetDetailsForm")) {
    const urlParams = new URLSearchParams(window.location.search);
    const taskSetId = parseInt(urlParams.get("taskSetId"));
    const taskSet = taskSets.find(ts => ts.id === taskSetId);

    if (taskSet) {
        document.getElementById("taskSetName").value = taskSet.name;

        document.getElementById("taskSetDetailsForm").addEventListener("submit", function(event) {
            event.preventDefault();
            taskSet.name = document.getElementById("taskSetName").value;
            document.getElementById("taskSetUpdateConfirmation").style.display = "block";
        });

        const taskList = document.getElementById("taskList");
        taskSet.tasks.forEach(task => {
            const listItem = document.createElement("li");
            listItem.textContent = task;
            taskList.appendChild(listItem);
        });
    }
}

function showConfirmation(event) {
    event.preventDefault(); // Prevent form submission for demonstration purposes

    // Get the input field values
    const id = document.getElementById("id").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    // Validate the inputs
    if (!id || !username || !password || !confirmPassword) {
        alert("Please fill out all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    //If all validations pass, show the confirmation message
    const confirmationMessage = document.getElementById("confirmationMessage");
    confirmationMessage.style.display = "block";
}

