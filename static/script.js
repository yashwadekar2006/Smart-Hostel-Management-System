// Smart Hostel Management System
// JavaScript File

console.log("Smart Hostel JavaScript Loaded");


// ==========================================
// Login Form Validation
// ==========================================

const loginForm = document.querySelector("#loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function(event) {

        const email = document.querySelector("#email").value.trim();
        const password = document.querySelector("#password").value.trim();

        if (email === "" || password === "") {

            alert("Please enter email and password.");

            event.preventDefault();
            return;
        }

        if (!email.includes("@")) {

            alert("Please enter a valid email address.");

            event.preventDefault();
            return;
        }

    });
}


// ==========================================
// Delete Student Confirmation
// ==========================================

const deleteForms = document.querySelectorAll(".delete-form");

deleteForms.forEach(function(form) {

    form.addEventListener("submit", function(event) {

        const confirmation = confirm(
            "Are you sure you want to delete this student?"
        );

        if (!confirmation) {

            event.preventDefault();

        }

    });

});


// ==========================================
// Add Student Form Validation
// ==========================================

const studentForm = document.querySelector("#studentForm");

if (studentForm) {

    studentForm.addEventListener("submit", function(event) {

        const name = document.querySelector("#name").value.trim();
        const email = document.querySelector("#student-email").value.trim();
        const phone = document.querySelector("#phone").value.trim();
        const roomNumber = document.querySelector("#room_number").value.trim();


        // Check empty fields
        if (
            name === "" ||
            email === "" ||
            phone === "" ||
            roomNumber === ""
        ) {

            alert("Please fill all student details.");

            event.preventDefault();
            return;
        }


        // Check email
        if (!email.includes("@")) {

            alert("Please enter a valid email address.");

            event.preventDefault();
            return;
        }


        // Check phone number
        if (!/^[0-9]{10}$/.test(phone)) {

            alert("Please enter a valid 10-digit phone number.");

            event.preventDefault();
            return;
        }

    });

}
// ==========================================
// Room Management - Show / Hide Students
// ==========================================

const roomTitles = document.querySelectorAll(".room-title");

roomTitles.forEach(function(title) {

    title.addEventListener("click", function() {

        const roomContent = title.nextElementSibling;

        if (roomContent.style.display === "none") {

            roomContent.style.display = "block";

        } else {

            roomContent.style.display = "none";

        }

    });

});

// ==========================================
// Fee Form Validation
// ==========================================

const feeForm = document.querySelector("#feeForm");

if (feeForm) {

    feeForm.addEventListener("submit", function(event) {

        const student = document.querySelector("#student_id").value;
        const amount = document.querySelector("#amount").value;
        const status = document.querySelector("#status").value;

        // Check empty fields
        if (student === "" || amount === "" || status === "") {

            alert("Please fill all fee details.");

            event.preventDefault();
            return;
        }

        // Check amount
        if (Number(amount) <= 0) {

            alert("Fee amount must be greater than 0.");

            event.preventDefault();
            return;
        }

    });

}