from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_FILE = os.path.join(os.getcwd(), "students.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        roll_number TEXT UNIQUE NOT NULL,
                        gender TEXT,
                        course TEXT,
                        joining_year INTEGER
                    )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    roll_number = request.form["roll_number"]
    gender = request.form["gender"]
    course = request.form["course"]
    joining_year = request.form["joining_year"]

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, roll_number, gender, course, joining_year) VALUES (?, ?, ?, ?, ?)",
                (name, roll_number, gender, course, joining_year))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
