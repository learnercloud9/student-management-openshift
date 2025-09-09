from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Use /tmp so SQLite can write in OpenShift container
DB_FILE = "/tmp/students.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            male TEXT,
            course TEXT,
            joining_year TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    number = request.form['number']
    male = request.form['male']
    course = request.form['course']
    joining_year = request.form['joining_year']
    gender = request.form['gender']

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, number, male, course, joining_year, gender) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, number, male, course, joining_year, gender))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8080)
