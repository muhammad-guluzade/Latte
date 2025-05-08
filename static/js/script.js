//Create Course Page (create_course.html)
if (document.getElementById("courseForm")) {
    document.getElementById("addTaskSet").addEventListener("change", function () {
        document.getElementById("taskSetSection").style.display = this.checked ? "block" : "none";
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

        let form = document.getElementById("courseForm");
        form.submit();
        document.getElementById("confirmationMessage").style.display = "block";
    });
}

var select_checker = 0;
//Generate Report Page (generate_report.html)
if (document.getElementById("reportForm")) {
    document.getElementById("reportForm").addEventListener("change", function () {
        let report_type_select = document.getElementById("reportType");
        let report_format_select = document.getElementById("reportFormat");
        let task_select = document.getElementById("taskSelectSection");

        const individualReportSection = document.getElementById("individualReportSection");
        const groupReportSection = document.getElementById("groupReportSection");

        if (!report_type_select.value || !report_format_select.value) {
            individualReportSection.style.display = "none";
            groupReportSection.style.display = "none";
            task_select.style.display = "none";
            select_checker = 0;
            return;
        }

        if (report_type_select.value === "individual") {
            individualReportSection.style.display = "block";
            groupReportSection.style.display = "none";
            task_select.style.display = "block";
            if(select_checker === 0){
                find_common_tasks();
                select_checker = 1;
            }

        } else if (report_type_select.value === "group") {
            individualReportSection.style.display = "none";
            groupReportSection.style.display = "block";
            task_select.style.display = "block";
            if(select_checker === 0){
                find_common_tasks();
                select_checker = 1;
            }
        }
    });

    document.getElementById("reportForm").addEventListener("submit", function (event) {
        event.preventDefault();
        let form = document.getElementById("reportForm");
        form.submit();
        document.getElementById("reportConfirmationMessage").style.display = "block";
    });
}

//View Courses Page (view_courses.html)
if (document.getElementById("courseList")) {

    const courseList = document.getElementById("courseList");
    courses.forEach(course => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${course}</span>
            <a href="/course_details/${course}">View Details</a>
        `;
        courseList.appendChild(listItem);
    });
}

//View Task Sets Page (view_task_sets.html)
if (document.getElementById("taskSetList")) {

    const taskSetList = document.getElementById("taskSetList");
    taskSets.forEach(taskSet => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${taskSet[1]}</span>
            <a href="/task_set_details/${taskSet[0]}">View Details</a>
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
        let form = document.getElementById("addStudentsForm");
        form.submit();
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

//Course Details Page
if (document.getElementById("courseDetailsForm")) {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = parseInt(urlParams.get("courseId"));

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
    const name = document.getElementById("name").value.trim();
    const surname = document.getElementById("surname").value.trim();
    const dob = document.getElementById("dateofbirth").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    let form = document.getElementById("signupForm");

    let terms_confirm = document.getElementById("confirm_terms");

    // Validate the inputs
    if (!name || !surname || !dob || !username || !password || !confirmPassword) {
        alert("Please fill out all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    if(!terms_confirm.checked){
        alert("Agree on the terms and conditions first.");
        return;
    }

    form.submit();
}

let inputs = document.getElementsByTagName("input");
for(let i = 0; i < inputs.length; i++){
    inputs[i].checked = false;
}
