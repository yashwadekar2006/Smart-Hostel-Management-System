from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# ==========================================
# MySQL Database Connection
# ==========================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mit@2025",
        database="hostel_management"
    )


# ==========================================
# Login Page
# ==========================================

@app.route("/")
def home():
    return render_template("login.html")


# ==========================================
# Login
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    if email == "admin@gmail.com" and password == "admin123":
        return render_template("admin_dashboard.html")

    elif email == "student@gmail.com" and password == "student123":
        return  render_template("student_dashboard.html")

    else:
        return "Invalid Email or Password!"

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")
# ==========================================
# Students Page + Search
# ==========================================

@app.route("/students")
def students():

    search = request.args.get("search", "")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search:

        query = """
            SELECT * FROM students
            WHERE name LIKE %s
            OR email LIKE %s
            OR room_number LIKE %s
        """

        search_value = "%" + search + "%"

        cursor.execute(
            query,
            (search_value, search_value, search_value)
        )

    else:

        cursor.execute(
            "SELECT * FROM students"
        )

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )


# ==========================================
# Add Student
# ==========================================

@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    room_number = request.form["room_number"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO students
        (name, email, phone, room_number)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, email, phone, room_number)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/students")


# ==========================================
# Edit Student
# ==========================================

@app.route("/edit_student/<int:id>")
def edit_student(id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    if student is None:
        return "Student not found!"

    return render_template(
        "edit_student.html",
        student=student
    )


# ==========================================
# Update Student
# ==========================================

@app.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    room_number = request.form["room_number"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        UPDATE students
        SET name = %s,
            email = %s,
            phone = %s,
            room_number = %s
        WHERE id = %s
    """

    cursor.execute(
        query,
        (name, email, phone, room_number, id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/students")


# ==========================================
# Delete Student
# ==========================================

@app.route("/delete_student/<int:id>", methods=["POST"])
def delete_student(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/students")


# ==========================================
# Room Management
# ==========================================

@app.route("/room_status")
def room_status():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM rooms ORDER BY room_number"
    )

    rooms = cursor.fetchall()

    for room in rooms:

        cursor.execute(
            """
            SELECT name, email, phone
            FROM students
            WHERE room_number = %s
            """,
            (room["room_number"],)
        )

        room["students"] = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "room_status.html",
        rooms=rooms
    )


# ==========================================
# Fees Management - View Fees
# ==========================================

@app.route("/fees")
def fees():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            fees.id,
            students.name,
            students.room_number,
            fees.amount,
            fees.status
        FROM fees
        INNER JOIN students
        ON fees.student_id = students.id
        ORDER BY fees.id DESC
    """

    cursor.execute(query)

    fee_records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "fees.html",
        fees=fee_records
    )


# ==========================================
# Add Fee Page
# ==========================================

@app.route("/add_fee")
def add_fee_page():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students ORDER BY name"
    )

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_fee.html",
        students=students
    )


# ==========================================
# Add Fee
# ==========================================

@app.route("/add_fee", methods=["POST"])
def add_fee():

    student_id = request.form["student_id"]
    amount = request.form["amount"]
    status = request.form["status"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO fees
        (student_id, amount, status)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (student_id, amount, status)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/fees")


# ==========================================
# Edit Fee Page
# ==========================================

@app.route("/edit_fee/<int:id>")
def edit_fee(id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM fees
        WHERE id = %s
        """,
        (id,)
    )

    fee = cursor.fetchone()

    cursor.close()
    connection.close()

    if fee is None:
        return "Fee record not found!"

    return render_template(
        "edit_fee.html",
        fee=fee
    )


# ==========================================
# Update Fee
# ==========================================

@app.route("/update_fee/<int:id>", methods=["POST"])
def update_fee(id):

    amount = request.form["amount"]
    status = request.form["status"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        UPDATE fees
        SET amount = %s,
            status = %s
        WHERE id = %s
    """

    cursor.execute(
        query,
        (amount, status, id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/fees")


# ==========================================
# Complaint Management
# ==========================================

@app.route("/complaints")
def complaints():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            complaints.id,
            students.name,
            students.room_number,
            complaints.complaint,
            complaints.status
        FROM complaints
        INNER JOIN students
        ON complaints.student_id = students.id
        ORDER BY complaints.id DESC
    """

    cursor.execute(query)

    complaint_records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "complaints.html",
        complaints=complaint_records
    )


# Submit Complaint
# ==========================================

@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():

    student_name = request.form["student_name"].strip()
    complaint = request.form["complaint"].strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id
        FROM students
        WHERE name = %s
        LIMIT 1
        """,
        (student_name,)
    )

    student = cursor.fetchone()

    if student is None:

        cursor.close()
        connection.close()

        return "Student not found! Please enter the correct student name."

    cursor.execute(
        """
        INSERT INTO complaints
        (student_id, complaint)
        VALUES (%s, %s)
        """,
        (student["id"], complaint)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/complaints")


# ==========================================
# Leave Request Management
# ==========================================

@app.route("/leave_requests")
def leave_requests():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            leave_requests.id,
            students.name,
            leave_requests.request_text
        FROM leave_requests
        INNER JOIN students
        ON leave_requests.student_id = students.id
        ORDER BY leave_requests.id DESC
    """

    cursor.execute(query)

    requests = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "leave_requests.html",
        requests=requests
    )


# ==========================================
# Submit Leave Request
# ==========================================

@app.route("/submit_leave_request", methods=["POST"])
def submit_leave_request():

    student_name = request.form["student_name"].strip()
    request_text = request.form["request_text"].strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Find student
    cursor.execute(
        """
        SELECT id
        FROM students
        WHERE name = %s
        LIMIT 1
        """,
        (student_name,)
    )

    student = cursor.fetchone()

    if student is None:

        cursor.close()
        connection.close()

        return "Student not found! Please enter the correct student name."

    # Save leave request
    cursor.execute(
        """
        INSERT INTO leave_requests
        (student_id, request_text)
        VALUES (%s, %s)
        """,
        (student["id"], request_text)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/leave_requests")


# ==========================================
# Notice Management
# ==========================================

@app.route("/notices")
def notices():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM notices ORDER BY id DESC"
    )

    notices = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "notices.html",
        notices=notices
    )


# ==========================================
# Add Notice
# ==========================================

@app.route("/add_notice", methods=["POST"])
def add_notice():

    title = request.form["title"].strip()
    notice_text = request.form["notice_text"].strip()

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO notices
        (title, notice_text)
        VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (title, notice_text)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/notices")


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)