from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Verbindung zur MySQL-Datenbank herstellen
db = mysql.connector.connect(
    host="localhost",  # Hostname der Datenbank
    user="your_username",  # Ihr Benutzername
    password="your_password",  # Ihr Passwort
    database="your_database"  # Name Ihrer Datenbank
)


@app.route('/')
def dashboard():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM theses")
    theses = cursor.fetchall()

    return render_template('dashboard.html', students=students, theses=theses)


@app.route('/student/create', methods=['POST'])
def create_student():
    name = request.form['student_name']
    cursor = db.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
    db.commit()
    return redirect('/')


@app.route('/student/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    name = request.form['name']
    cursor = db.cursor()
    cursor.execute("UPDATE students SET name = %s WHERE id = %s", (name, student_id))
    db.commit()
    return redirect('/')


@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    db.commit()
    return redirect('/')


@app.route('/thesis/create', methods=['POST'])
def create_thesis():
    title = request.form['title']
    student_id = int(request.form['student_id'])
    cursor = db.cursor()
    cursor.execute("INSERT INTO theses (title, student_id) VALUES (%s, %s)", (title, student_id))
    db.commit()
    return redirect('/')


@app.route('/thesis/edit/<int:thesis_id>', methods=['POST'])
def edit_thesis(thesis_id):
    title = request.form['title']
    cursor = db.cursor()
    cursor.execute("UPDATE theses SET title = %s WHERE id = %s", (title, thesis_id))
    db.commit()
    return redirect('/')


@app.route('/thesis/delete/<int:thesis_id>')
def delete_thesis(thesis_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM theses WHERE id = %s", (thesis_id,))
    db.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
