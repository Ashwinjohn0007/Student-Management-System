from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

ADMIN_ID = "admin"
ADMIN_PASSWORD = "1234"
CSV_FILE = "students.csv"

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("login.html")

# ---------------- STUDENT LOGIN ----------------
@app.route('/student_login', methods=['POST'])
def student_login():
    roll = request.form.get("roll")

    if not os.path.exists(CSV_FILE):
        return "No student records found"

    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["roll"] == roll:
                session["student"] = row
                return redirect(url_for("student_dashboard"))

    return "Invalid Roll Number"

# ---------------- STUDENT DASHBOARD ----------------
@app.route('/student_dashboard')
def student_dashboard():
    if "student" in session:
        return render_template("student_dashboard.html", data=session["student"])
    else:
        return redirect(url_for("home"))

# ---------------- ADMIN LOGIN PAGE ----------------
@app.route('/admin')
def admin():
    return render_template("admin_login.html")

# ---------------- ADMIN LOGIN CHECK ----------------
@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_id = request.form.get("admin_id")
    password = request.form.get("password")

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
        session["admin"] = True
        return redirect(url_for("admin_dashboard"))
    else:
        return "Invalid Admin Credentials"

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if "admin" in session:
        return render_template("admin_dashboard.html")
    else:
        return redirect(url_for("admin"))

# ---------------- ADD STUDENT ----------------
@app.route('/add_student', methods=['POST'])
def add_student():

    if "admin" not in session:
        return redirect(url_for("admin"))

    roll = request.form.get("roll")
    name = request.form.get("name")
    total_fees = int(request.form.get("total_fees"))

    sem1 = int(request.form.get("sem1"))
    sem2 = int(request.form.get("sem2"))
    sem3 = int(request.form.get("sem3"))
    sem4 = int(request.form.get("sem4"))
    sem5 = int(request.form.get("sem5"))
    sem6 = int(request.form.get("sem6"))
    sem7 = int(request.form.get("sem7"))
    sem8 = int(request.form.get("sem8"))

    total_paid = sem1+sem2+sem3+sem4+sem5+sem6+sem7+sem8
    total_pending = total_fees - total_paid

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "roll","name","total_fees","total_paid","total_pending",
                "sem1","sem2","sem3","sem4","sem5","sem6","sem7","sem8"
            ])

        writer.writerow([
            roll,name,total_fees,total_paid,total_pending,
            sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8
        ])

    return redirect(url_for("admin_dashboard"))

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)