from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguration für die Verbindung zur MySQL-Datenbank
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user_version_1:pw_version_1@localhost/ba_version_1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definition der Datenbankmodelle für Studenten und Abschlussarbeiten
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    matrikelnummer = db.Column(db.String(20))
    email = db.Column(db.String(255))


class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student', backref=db.backref('theses', lazy=True))


@app.route('/')
def dashboard():
    students = Student.query.all()
    theses = Thesis.query.all()
    return render_template('dashboard.html', students=students, theses=theses)


@app.route('/student/create', methods=['POST'])
def create_student():
    name = request.form['student_name']
    matrikelnummer = request.form['matrikelnummer']
    email = request.form['email']
    student = Student(name=name, matrikelnummer=matrikelnummer, email=email)
    db.session.add(student)
    db.session.commit()
    return redirect('/')


@app.route('/student/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)
    student.name = request.form['name']
    db.session.commit()
    return redirect('/')


@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')


@app.route('/thesis/create', methods=['POST'])
def create_thesis():
    title = request.form['title']
    student_id = int(request.form['student_id'])
    student = Student.query.get(student_id)
    thesis = Thesis(title=title, student=student)
    db.session.add(thesis)
    db.session.commit()
    return redirect('/')


@app.route('/thesis/edit/<int:thesis_id>', methods=['POST'])
def edit_thesis(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    thesis.title = request.form['title']
    thesis.student_id = request.form['student_id']
    db.session.commit()
    return redirect('/')


@app.route('/thesis/delete/<int:thesis_id>')
def delete_thesis(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    db.session.delete(thesis)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
